# Dedication Tracker
Tracks work done on tasks via time (with a timer) or integer/decimal units each day.  
Displays stats in a basic format, or a customizable graph.

# Dedication_Tracker.pyw

![image_2022-09-20_220050754](https://user-images.githubusercontent.com/19754911/191404733-99483a9d-719d-4f9d-a170-706729d71f98.png)

Enter a category name in the entry space on the left, and click "Add new category" to add it to the list.

Use the tab on the bottom-right to select a category.

"Switch to number mode" and "Switch to time mode" toggle between time and number mode.

In time mode, click "Start" to start adding time. Click "Pause" to stop adding time.

In number mode, enter a value in the center entry field, and click "Update" to set that category's number value for the current day.

The timer in time mode can be left running while performing an activity for which you would like to record participation time (e.g. studying).

Number mode can be used to record activities that are defined in integers or decimals (e.g. number of push-ups completed that day). 

Timer mode saves data automatically.

Click "Basic View" to bring up a list of dates with their corresponding time/number values for categories that have data for those days.

"Delete category" brings up a list of all saved categories, which can be deleted from there. Note that deleting a category does not currently remove all of its entries from the data file.

Click "Create Graph" to open the graph creator.


# Dedication_Graph_Creator.pyw

Runs the graph creator as a standalone window.

Standalone mode still uses the data files created by the main Dedication Tracker. 

![image_2022-09-20_221514636](https://user-images.githubusercontent.com/19754911/191406439-27ba2e09-fa36-4d10-ab02-ff90ff8825e0.png)

**Set start date**/**Set end date**: Explicitly define starting and ending points for the dates included in the graph. Can only be used when "Duration setting" is set to "Date range".

**Start how many days ago**: Define the starting point of the graph as x number of days in the past (including today as the first day), with x being the value in the spinbox below. Can only be used when "Duration setting" is set to "Days ago" (default).

**Duration setting**: Defines how the date range to be graphed will be chosen, between "Days ago" (default), "Date range", and "All" (all recorded dates).

**Exclude current day**: When checked, does not include results for the current date in the graph.

**Empty values are displayed as**: When a date contains no data for a chosen category, it will display either a value of "Zero" or "Nil"(leaves data point blank).

**Nil value range**: Defines whether the graph date range should be constricted if there are only "Nil" values on its left and/or right borders. "All" (default) does nothing, "Left" preserves empty space only on the left, "Right" preserves empty space only on the right, and "Min" preserves the minimum amount of empty space possible.

**Graph type**: Set the graph to use data points from either "Time" or "Number" mode.

**Min Value**/**Max value**: Choose between "Automatic" (default) and "Manual" definition of the graph's vertical borders. Time mode allows explicit specification of minimum and maximum values in hours, minutes, and seconds with the spinboxes below each. Number mode allows specification of an integer value for each bound.

**Target value(s)**: Optionally specify one or two target lines (horizontal dark lines) to be drawn across the graph at the defined hour/integer positions. Can be used, for example, to specify a minimum value and target value for a particular activity. Does nothing if set to "None" or 0.

**Plot rolling average**: Add a line following the rolling average of the graph data. Only applies to the first category selected. "Nil" values are treated as 0 by rolling average.

**Rolling average interval (days)**: Specify the interval (in days) over which the rolling average(s) should be calculated. E.g. setting it to 7 would cause the rolling average line to reset every seven days on the graph. Does nothing if set to 1. Covers the entire graph without resetting if set to "All" or 0.

**Add/remove graph categories**: Select a category from the chosen mode (Time/Number), and click "Add" to add it to the categories to be graphed. Click "Remove" to remove it.

**Graph categories**: Contains a list of all categories to be used in the current graph.

**Color**: Contains a list of the corresponding color that each category will be displayed with on the graph. Colors set to "Auto" will be chosen automatically.

**Line style**: Contains a list of the corresponding line style ("dot style") that each category will be displayed with on the graph.

**Color select mode**: Toggle between "Automatic" and "Manual" color assignment for graph categories.

**Choose color**: Manually specify the active color. Can only be used in "Manual" color mode.

**Overwrite selected color**: Click on a color from the "Color" list to highlight it, and click "Overwrite selected color" to replace that color with the active color, or "Auto" if set to "Automatic" mode.

**Overwrite selected style**: Click on a style from the "Line style" list to highlight it, and click "Overwrite selected style" to replace it with the current "Line dot style" and "Line style".

**Graph format**: Choose between "Line" and "Bar" graphs. "Line" plots daily values on a line across time. "Bar" plots categories as bars with their height being equal to their total time/number values for the selected time period. Certain options are not applicable and will be grayed out in "Bar" mode.

**Line dot style**: Choose the type of dot to represent each data point with in "Line" mode. "Flat" (default) does not display individual data points as dots on the line.

**Line style**: Choose a style for the line in "Line" mode. "solid" (default) is a normal line. "None" displays no line, and will only be visible if "Line dot style" is set to something other than "Flat".

**Graph name**: Enter a name for the graph in the entry box below. Graph names are optional for normal graphing.

**Save configuration to file**: Save all selected options to the config file. A graph name is required to save a configuration.

**Load configuration from file**: Select a saved configuration by name from the config file. "Direct graph" creates a graph on the spot using those settings (note that a relative date range with "Days ago" will not necessarily display the same results as when the configuration was originally saved). "Select" overwrites selected options with those saved in the configuration. "Delete" deletes the highlighted configuration from the file.

**Create graph**: Creates a graph from the chosen configuration options.
