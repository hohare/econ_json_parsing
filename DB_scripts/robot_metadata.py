import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime

def parse_log(file_path):
    events = []
    with open(file_path, 'r') as file:
        for line in file:
            timestamp_str, action = line.split(' INFO: ')
            timestamp = datetime.datetime.strptime(timestamp_str, '[%Y-%m-%d %H:%M:%S,%f]')
            events.append((timestamp, action.strip()))
    return events




def plot_events(events, output_file):
    fig, ax = plt.subplots(figsize=(15, 8))

    y_labels = ['Robot B', 'Hexacontroller socket B', 'Robot A', 'Hexacontroller socket A', ""]
    y_positions = {label: i for i, label in enumerate(y_labels)}

    # Get the first timestamp to calculate minutes since the start
    start_time = events[0][0]

    robot_time = 0
    hexa_time = 0
    counter = 0

    for timestamp, action in events:
        #print(f"Processing event: {timestamp} - {action}")  # Debug print
        minutes_since_start = (timestamp - start_time).total_seconds() / 60.0
        if 'Start test' in action:
            if 'A' in action:
                end_time = minutes_since_start + 2 + 40 / 60.0
                ax.add_patch(patches.Rectangle((minutes_since_start, y_positions['Hexacontroller socket A']), end_time - minutes_since_start, 1.0, color='blue', alpha=0.5))
                hexa_time+= end_time - minutes_since_start
                counter += 1 
            elif 'B' in action:
                end_time = minutes_since_start + 2 + 40 / 60.0
                ax.add_patch(patches.Rectangle((minutes_since_start, y_positions['Hexacontroller socket B']), end_time - minutes_since_start, 1.0, color='blue', alpha=0.5))
                hexa_time+= end_time - minutes_since_start
                counter+=1

        elif 'Start move' in action and 'to A' in action:
            move_start_time = minutes_since_start
        elif 'Done move' in action and 'to A' in action:
            move_end_time = minutes_since_start
            ax.add_patch(patches.Rectangle((move_start_time, y_positions['Robot A']), move_end_time - move_start_time, 1.0, color='green', alpha=0.5))
            robot_time += move_end_time - move_start_time
        elif 'Start move' in action and 'to B' in action:
            move_start_time = minutes_since_start
        elif 'Done move' in action and 'to B' in action:
            move_end_time = minutes_since_start
            ax.add_patch(patches.Rectangle((move_start_time, y_positions['Robot B']), move_end_time - move_start_time, 1.0, color='green', alpha=0.5))
            robot_time += move_end_time - move_start_time

        elif 'Start return' in action and 'from A' in action:
            return_start_time = minutes_since_start
        elif 'Done return' in action and 'from A' in action:
            return_end_time = minutes_since_start
            ax.add_patch(patches.Rectangle((return_start_time, y_positions['Robot A']), return_end_time - return_start_time, 1.0, color='red', alpha=0.5))
            robot_time += return_end_time - return_start_time

        elif 'Start return' in action and 'from B' in action:
            return_start_time = minutes_since_start
        elif 'Done return' in action and 'from B' in action:
            return_end_time = minutes_since_start
            ax.add_patch(patches.Rectangle((return_start_time, y_positions['Robot B']), return_end_time - return_start_time, 1.0, color='red', alpha=0.5))
            robot_time += move_end_time - move_start_time


    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)

    #ax.set_yticklabels([''] * len(y_labels))  # Remove default y-axis labels
    ax.set_xlabel('Minutes since start')
    ax.set_ylabel('Actions')

    # Set x-axis to display the correct range of minutes since start
    max_minutes = (events[-1][0] - start_time).total_seconds() / 60.0
    ax.set_xlim(0, max_minutes)

    # Add centered y-axis labels
    #for label, position in y_positions.items():
    #    ax.text(-5, position, label, va='center', ha='right', fontsize=12, rotation=0, transform=ax.get_yaxis_transform())

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    print(robot_time, hexa_time)
    print(robot_time - hexa_time, counter, (robot_time - hexa_time) * 60 / counter)
    plt.show()

# Example usage
events = parse_log('runner_log.log')
plot_events(events, 'robot_actions_plot_all.png')