import csv
import uuid
from station import Station
from ticket import Ticket

def ls(f):
    stations = {}
    with open(f, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stations[row['name']] = Station(row['id'], row['name'], row['lines'])
    return stations

def lc(f):
    graph = {}
    with open(f, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fr = row['from_station']
            to = row['to_station']
            if fr not in graph:
                graph[fr] = []
            if to not in graph:
                graph[to] = []
            graph[fr].append(to)
            graph[to].append(fr)
    return graph

def prices(path):
    return 100 + 50*(len(path) - 1)

def pathmain(graph, start, end):
    stack = [(start, [start])]
    all_paths = []
    while stack:
        current, path = stack.pop()
        if current == end:
            all_paths.append(path)
        else:
            for neighbor in graph.get(current, []):
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))
    if all_paths:
        shortest = min(all_paths, key=len)
        return shortest
    else:
        return []



def lines(stations, path):
    if not path or len(path) < 2:
        return "No transfers needed."
    last_line = None
    instructions = []
    for i in range(len(path)):
        cur_station = stations[path[i]]
        lines_here = cur_station.lines
        if i == 0:
            last_line = lines_here[0]
            instructions.append(f"Start at {cur_station.name} on {last_line} Line.")
        else:
            prev_station = stations[path[i-1]]
            shared_lines = set(prev_station.lines).intersection(set(lines_here))
            if last_line not in shared_lines:
                change_at = cur_station.name
                possible_lines = ','.join(lines_here)
                instructions.append(f"Change at {change_at} to {possible_lines} Line.")
                last_line = lines_here[0]
    instructions.append(f"Arrive at {path[-1]}.")
    return " ".join(instructions)

def show(stations):
    print("\nAvailable Metro Stations:")
    for station in stations.values():
        print(f"{station.name} ({', '.join(station.lines)})")
    print()

def tickets(f):
    import csv
    with open(f, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print("\nYour Tickets:")
        for row in reader:
            print(
                "ID: " + row['ticket_id'] +
                " | From: " + row['from_station'] +
                " | To: " + row['to_station'] +
                " | Price: " + row['price'] +
                " | Path: " + row['path'] +
                " | Instructions: " + row['instructions']
            )


def ticketsmain(ticket, f):
    with open(f, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            ticket.ticket_id,
            ticket.from_station,
            ticket.to_station,
            ticket.price,
            '|'.join(ticket.path),
            ticket.instructions
        ])

def main():
    stations = ls('stations.csv')
    graph = lc('connections.csv')
    while True:
        print("\nMetro Ticket System")
        print("1. Show Metro Stations")
        print("2. Buy Ticket")
        print("3. View Tickets")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            show(stations)
        elif choice == "2":
            from_station = input("Enter starting station: ").upper()
            to_station = input("Enter destination station: ").upper()
            if from_station not in stations or to_station not in stations:
                print("Invalid station name!")
                continue
            path = pathmain(graph, from_station, to_station)
            if not path:
                print("No route found!")
                continue
            price = prices(path)
            instructions = lines(stations, path)
            ticket_id = str(uuid.uuid4())
            ticket = Ticket(ticket_id, from_station, to_station, price, path, instructions)
            ticketsmain(ticket, 'tickets.csv')
            print(f"Ticket purchased! ID: {ticket_id}")
            print(f"Route: {' -> '.join(path)}")
            print(f"Price: Rs. {price}")
            print(f"Instructions: {instructions}")
        elif choice == "3":
            tickets('tickets.csv')
        elif choice == "4":
            print("Thank you for using the Metro Ticket System!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")
            break
main()
