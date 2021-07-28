import tkinter
from tkinter import filedialog
import pandas as pd
from matplotlib.pyplot import *


def get_file():
    my_window = tkinter.Tk()                                        # initialize window example
    my_window.title("MVS(map visualization system)")                # rename the window
    my_window.geometry('400x300')                                   # control window size
    my_window.resizable(width=True, height=True)                    # set the window resizable
    file_path = filedialog.askopenfilename()                        # open file manager
    suffix = file_path.split(".")[len(file_path.split("."))-1]      # get suffix
    if suffix == "xls" or "csv" or "xlsx":                          # confirm suffix as "xls" or "csv" or "xlsx"
        return file_path
    else:
        return 0


def get_data(certain_file):
    """
    Read the required data. Should be modified if data name or requirement is changed.
    :param certain_file: file path
    :return: type:numpy.n-dimension array
    """
    df = pd.read_excel(certain_file)
    data = df.loc[:, ["t[s]", "HMI_Right_ObstaclePosY_mp[]", "HMI_Right_ObstaclePosX_mp[]",
                      "HMI_Left_ObstaclePosY_mp[]", "HMI_Left_ObstaclePosX_mp[]",
                      "HMI_CIPV_ObstaclePosY_mp[]", "HMI_CIPV_ObstaclePosX_mp[]",
                      "LAP_Path_Pred_First_C3_YJ_mp[]", "LAP_Path_Pred_First_C2_YJ_mp[]",
                      "LAP_Path_Pred_First_C1_YJ_mp[]", "LAP_Path_Pred_First_C0_YJ_mp[]"]].values
    return data


def plot_func(input_data):
    """
    use mp to plot obstacles and center lane.
    :param input_data: data got from file.
    :return: null
    """
    time_arr = input_data[:, 0].tolist()
    cubic_curve_c3 = input_data[:, 7].tolist()
    cubic_curve_c2 = input_data[:, 8].tolist()
    cubic_curve_c1 = input_data[:, 9].tolist()
    cubic_curve_c0 = input_data[:, 10].tolist()

    right_obstacle_pos_arr_y = input_data[:, 1].tolist()
    right_obstacle_pos_arr_x = input_data[:, 2].tolist()
    left_obstacle_pos_arr_y = input_data[:, 3].tolist()
    left_obstacle_pos_arr_x = input_data[:, 4].tolist()
    cipv_obstacle_pos_arr_y = input_data[:, 5].tolist()
    cipv_obstacle_pos_arr_x = input_data[:, 6].tolist()
    x_max = max(max(right_obstacle_pos_arr_x, left_obstacle_pos_arr_x, cipv_obstacle_pos_arr_x))
    x_min = min(min(right_obstacle_pos_arr_x, left_obstacle_pos_arr_x, cipv_obstacle_pos_arr_x))
    y_max = max(max(right_obstacle_pos_arr_y, left_obstacle_pos_arr_y, cipv_obstacle_pos_arr_y))
    y_min = min(min(right_obstacle_pos_arr_y, left_obstacle_pos_arr_y, cipv_obstacle_pos_arr_y))

    figure()
    title("center lane")
    xlabel("y")
    ylabel("x")
    grid()
    axes_scat = gca()
    axes_scat.set_xlim([y_min, y_max])
    axes_scat.set_ylim([x_min, x_max])

    x = np.linspace(x_min, x_max, 100)
    for i in range(len(time_arr) - 1):
        # cubic curve at present
        c0 = cubic_curve_c0[i]
        c1 = cubic_curve_c1[i]
        c2 = cubic_curve_c2[i]
        c3 = cubic_curve_c3[i]

        # cubic curve representation
        y = c0 + c1*x + c2*x**2 + c3*x**3

        # plot obstacle position
        scat_plot_right = scatter(right_obstacle_pos_arr_y[i], right_obstacle_pos_arr_x[i], c='purple')
        scat_plot_left = scatter(left_obstacle_pos_arr_y[i], left_obstacle_pos_arr_x[i], c='red')
        scat_plot_center = scatter(cipv_obstacle_pos_arr_y[i], cipv_obstacle_pos_arr_x[i], c='black')
        center_lane_plot, = plot(y, x, "r*")


        legend([scat_plot_right, scat_plot_left, scat_plot_center, center_lane_plot], ["right obstacle point",
                                                                                       "left obstacle point",
                                                                                       "center obstacle point",
                                                                                       "center lane"],
               loc="upper right",
               scatterpoints=1)

        pause(time_arr[i+1] - time_arr[i])
        center_lane_plot.remove()
        scat_plot_right.remove()
        scat_plot_left.remove()
        scat_plot_center.remove()


if __name__ == "__main__":
    file = get_file()
    my_data = get_data(file)
    # plot_obstacle_pos(my_data)
    plot_func(my_data)
    pass
