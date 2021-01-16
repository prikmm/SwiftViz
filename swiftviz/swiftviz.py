import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import copy as cp


class CustomPalette():

    def __init__(self):
        self.current_palette = sns.color_palette()


    @staticmethod
    def display_palette(custom_colors, *args, **kwargs):
        custom_palette = sns.color_palette(custom_colors, *args, **kwargs)
        sns.palplot(custom_palette, size=0.8)
        plt.tick_params(axis='both', labelsize=0, length = 0)


    @staticmethod
    def set_default_custom_palette(custom_colors, *args, **kwargs):
        custom_palette = sns.color_palette(custom_colors, *args, **kwargs)
        sns.set_palette(custom_palette)

    

class Plotter():

    def __init__(self):
        pass
    
    @staticmethod
    def col_axis_generator(rows, cols):
        col_list = np.arange(cols)
        col_str = ''.join(str(e) for e in col_list)
        col_str *= rows
        col_array = np.int64(np.array(list(col_str)))
        return col_array
    # Return Value: [0 1 2 3 4 0 1 2 3 4] for rows=2, cols=5


    @staticmethod
    def row_axis_generator(rows, cols):
        row_array = np.repeat(np.sort(np.arange(rows)), cols)
        return row_array
    # Return Value: [0 0 0 0 0 1 1 1 1 1] for rows=2, cols=5

    @classmethod
    def row_col_merge(cls, rows, cols):
        row_axis = cls.row_axis_generator(rows, cols)
        col_axis = cls.col_axis_generator(rows, cols)
        axis = np.c_[row_axis, col_axis]
        return axis
    # Return Value: [[0 0]
    #                [0 1]
    #                  .
    #                  .
    #                  .
    #                [1 4]]
    # For rows=2, cols=5

    def __datatype_handler(self, ys, cat_vars):
        variables = [ys, cat_vars]
        for i, var in enumerate(variables):
            if type(var) != 'numpy.ndarray':
                if len(var) == 1:
                    variables[i] = np.array([var])
                else:
                    variables[i] = np.array(var)
        ys = variables[0]
        cat_vars = variables[1]
        return ys, cat_vars

    def complete_axis_generator(self, ys, cat_vars, rows, cols):
        
        ys, cat_vars = self.__datatype_handler(ys, cat_vars)
        axis = self.row_col_merge(rows, cols)
        row_axis = axis[:, 0]
        col_axis = axis[:,1]
        variables = [(ys, col_axis), (cat_vars, row_axis)]
        for i, var_axis in enumerate(variables):
            var = var_axis[0]
            axis = var_axis[1]
            if var.size == 1:
                variables[i] = np.repeat(var, len(row_axis))
                
            else:
                variables[i] = var[axis]    

        y_arr, cat_arr = variables
        axis = np.c_[cat_arr, y_arr, row_axis, col_axis]
        return axis
    # Return Value:[[cat_arr[0] y_arr[0] 0 0],
    #                cat_arr[0] y_arr[1] 0 1],
    #                          .
    #                          .
    #                          .
    #                [cat_arr[1] y_arr[4] 1 4]]
    # for len(cat_arr) = 2, len(y_arr) = 5, rows=2, cols=5


    # Main Function: We will use this function to quickly skim over the relations of features,
    #                then zoom in on the once we feel give us some insights
    def plotter(self, df, x, ys, cat_vars, fig_width=30, fig_height=10):

        ys, cat_vars = self.__datatype_handler(ys, cat_vars)
        rows = cat_vars.size
        cols = ys.size
        fig, axs = plt.subplots(figsize=(fig_width, fig_height), nrows=rows, ncols=cols)
        
        axis = self.complete_axis_generator(ys, cat_vars, rows, cols)
        for cat_var, y, row, col in axis:
            row = np.int64(row)
            col = np.int64(col)

            if len(axs.shape) == 1:
                sns.scatterplot(x=df[x], y=df[y], hue=df[cat_var], ax=axs[row | col])
                axs[row | col].set_title(f'{x} v/s {y} for {cat_var}')
            else:
                sns.scatterplot(x=df[x], y=df[y], hue=df[cat_var], ax=axs[row, col])
                axs[row, col].set_title(f'{x} v/s {y} for {cat_var}')

        fig.suptitle(f'Plots for {x}')



class Encoder():

    def __init__(self):
        pass

    def column_encoder(self, df, x, inplace=False):
        key_dict = dict()
        operated_df = None
        if inplace:
            operated_df = df
        else:
            operated_df = cp.deepcopy(df)

        for col in np.arange(len(x)):
            uniq_vals = operated_df[x[col]].unique()
            encoding_vals = np.arange(len(uniq_vals))
            replace_arr = np.array(tuple(zip(uniq_vals, encoding_vals)))
            key_dict[x[col]] = replace_arr
            operated_df[x[col]].replace(to_replace=replace_arr[:, 0], value=replace_arr[:, 1], inplace=True)

        if inplace:
            return key_dict
        else:
            return operated_df, key_dict



class PieCompositionPlots():
    
    def __init__(self, df, x):
        self.df = df
        self.x = x
        self.uni_list = np.sort(self.df[self.x].unique())


    def cat_count_generator(self, cat_variables, verbo=0):
        self.cat_counts = list()
        print("Cat_counts array at beginning:{cat_counts}\n".format(cat_counts=self.cat_counts) if verbo else '', end='')
        for cat_var in cat_variables:
            dumm_arr = np.array([])
            print("For {cat_var}:\n".format(cat_var=cat_var) if verbo else '', end='')
            cat_uni_list = np.sort(self.df[cat_var].unique())
            print("Unique values: {cat_uni_list}\n".format(cat_uni_list=cat_uni_list) if verbo else '', end='')
            for uni_val in self.uni_list:
                print("Checking for {uni_val}:\n".format(uni_val=uni_val) if verbo else '', end='')
                for cat_uni_val in cat_uni_list:
                    dumm_arr = np.r_[dumm_arr, np.sum(self.df[self.df[self.x] == uni_val][cat_var] == cat_uni_val)]
                    print("Arr for {cat_uni_val}: {dumm_arr}\n".format(cat_uni_val=cat_uni_val, dumm_arr=dumm_arr) if verbo else '', end='')
            self.cat_counts.append(dumm_arr)
            print("Final arr after each loop: {cat_counts}\n".format(cat_counts=self.cat_counts) if verbo else '', end='')

    @staticmethod
    def __cat_axis_generator(rows, cols):
        cat_axis = Plotter.row_col_merge(rows, cols)
        return cat_axis


    def __explode_list_handler(self, cat_variables, explode_list, cat_num):
        flag = 0
        if not explode_list:
            explode_list = list()
            flag = 1

        cat_explode_diff = len(explode_list) - cat_num 
        for cat_var in cat_variables[cat_explode_diff:]:
            inner_dim = len(self.df[cat_var].unique()) * len(self.uni_list)
            explode_list.append([0]*inner_dim)
        if flag:
            return explode_list

    
    def __cat_complete_axis_generator(self, cat_variables, labels, cols=2, explode_list=None, verbo=0):

        cat_num = len(cat_variables)
        if cat_num < cols:
            cols = cat_num
        
        rows = None
        if cols != cat_num and cat_num % cols ==0:
            rows = int(cat_num/cols)
        elif cols != cat_num and cat_num % cols !=0:
            rows = int(cat_num/cols) + 1
        else:
            rows = 1

        self.cat_count_generator(cat_variables, verbo=verbo)
        axis = self.__cat_axis_generator(rows, cols)

        
        if explode_list and len(explode_list) < cat_num:
            self.__explode_list_handler(cat_variables, explode_list, cat_num)
        if not explode_list:
            explode_list = self.__explode_list_handler(cat_variables, explode_list, cat_num)

        complete_axis = list(zip(axis, cat_variables, labels, self.cat_counts, explode_list))
        return complete_axis, rows, cols
    
    def pie_plotly(self, cat_variables, labels, cols=2, width=800, height=600, explode_list=None, verbo=0, color_theme=None, **kwargs):

        complete_axis, rows, cols = self.__cat_complete_axis_generator(cat_variables, labels, 
                                                                       cols=cols, explode_list=explode_list, verbo=verbo)
        spec_list = [[{'type': 'pie'}]*cols for i in range(rows)]
        fig = make_subplots(rows=rows, cols=cols, specs=spec_list)
        for axis, cat_var, cat_labels, counts, pull_para in complete_axis:
            row = axis[0]+1
            col = axis[1]+1
            fig.add_trace(go.Pie(values=counts,
                                labels=cat_labels,
                                title=f'{cat_var}',
                                name=f'{cat_var}',
                                showlegend=True, pull=pull_para, **kwargs), 
                                row=row, col=col)     

        fig.update_layout(title=f'{self.x} Composition',
                          autosize=False, 
                          width=width, height=height)

        if color_theme:
            fig.layout.template = color_theme

        fig.show()

    def pie_mat(self, cat_variables, labels, cols=2, figsize=(30, 10), explode_list=None, white_radius=0.4, **kwargs):

        complete_axis, rows, cols = self.__cat_complete_axis_generator(cat_variables, labels, cols=cols, explode_list=explode_list)
        fig, axs = plt.subplots(figsize=figsize, nrows=rows, ncols=cols)

        for axis, cat_var, cat_labels, counts, explode in complete_axis:
  
            row = axis[0]
            col = axis[1]

            if len(axs.shape) == 1:
                axs[row | col].pie(counts, labels=cat_labels, explode=explode, **kwargs)
                axs[row | col].set_title(f'{cat_var}')
                axs[row | col].add_artist(plt.Circle((0,0), white_radius,fc='white'))
            else:
                axs[row, col].pie(counts, labels=cat_labels, explode=explode, **kwargs)
                axs[row, col].set_title(f'{cat_var}')
                axs[row, col].add_artist(plt.Circle((0,0), white_radius,fc='white'))

        fig.title(f'{self.x} Composition for Various Categorical Variables')



class CatComposition():

    def __init__(self, df):
        self.df = df


    @staticmethod
    def __composition_axis_generator(cat_variables, cols):
        
        cat_num = len(cat_variables)
        if cat_num < cols:
            cols = cat_num

        rows = None
        if cols != cat_num and cat_num % cols ==0:
            rows = int(cat_num/cols)
        elif cols != cat_num and cat_num % cols !=0:
            rows = int(cat_num/cols) + 1
        else:
            rows = 1
        axis = Plotter.row_col_merge(rows, cols)
        complete_axis = list(zip(axis, cat_variables))
        return complete_axis, rows, cols


    def bar_composition(self, cat_variables, cols=2, figsize=(30, 10), **kwargs):
        complete_axis, rows, cols = self.__composition_axis_generator(cat_variables, cols)
        print(len(complete_axis))
        print(complete_axis)
        fig, axs = plt.subplots(figsize=figsize, nrows=rows, ncols=cols)

        for axis, cat_var in complete_axis:
            row = axis[0]
            col = axis[1]

            if len(axs.shape) == 1:
                sns.catplot(data=self.df, x=cat_var, kind='count', **kwargs, ax=axs[row | col])
                axs[row | col].set_title(f'{cat_var}')
            else:
                sns.catplot(data=self.df, x=cat_var, kind='count', **kwargs, ax=axs[row, col])
                axs[row, col].set_title(f'{cat_var}')

        fig.set_title('Categorical Variables Composition')



class OutlierAnalysis():

    def __init__(self, df):
        self.df =df


    def data_scaler(self, num_vars):
        scaled_df = (self.df[num_vars] - self.df[num_vars].mean())/self.df[num_vars].std()
        return scaled_df

    def OutlierReport(self, num_vars):
        quantile_report = np.array(self.df[num_vars].quantile([0.25, 0.75]).T)
        iqr_report = quantile_report[:, 1] - quantile_report[:, 0]
        min_max_report = np.c_[np.array(self.df[num_vars].min()), np.array(self.df[num_vars].max())]
        median_report = np.array(self.df[num_vars].median())
        left_whisker_limit = quantile_report[:, 0] - (1.5*iqr_report)
        right_whisker_limit = quantile_report[:, 1] + (1.5*iqr_report)
        left_outliers = np.sum(self.df[num_vars] < left_whisker_limit)
        right_outliers = np.sum(self.df[num_vars] > right_whisker_limit)
        total_outliers = left_outliers + right_outliers
        outlier_report = pd.DataFrame(np.array([median_report,
                                                min_max_report[:, 0], min_max_report[:, 1],
                                                quantile_report[:, 0], quantile_report[:, 1],
                                                iqr_report,
                                                left_whisker_limit, right_whisker_limit,
                                                left_outliers, right_outliers,
                                                total_outliers]),
                                    index=['median', 'min', 'max', '25%', '75%', 'IQR',
                                            'Left Whisker Limit', 'Right Whisker Limit',
                                            'No.of Left Outliers', 'No.of Right Outliers',
                                            'Total Outliers'],
                                    columns=num_vars)                       
        return outlier_report
