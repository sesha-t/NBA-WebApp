import mysql.connector # I use this library to connect to connect to the database
quit = 0
message_list = []
team_list = []
line_count = 0
mydb = mysql.connector.connect(host="localhost", database = 'nba',user="task", password="password123", auth_plugin='mysql_native_password')
mycursor = mydb.cursor(buffered=True)  # This first cursor is to check if the name the user inputs actually exists in db
other_cursor = mydb.cursor(buffered=True)  # This cursor is for executing what the user wants

def temp_function(name):  # function that contains all the executions that is called in the while loop below
    team_list.clear()    # clears the list everytime the function is called is case user enters the same name and selection twice
    line_count = 0
    my_points = 0
    number_of_repetitions = 0

    try:
        second_message = int(input("Make a selection of what you want to do:" + "\n" + "1. Get the years " + name.title()

                               + " played in his career " + "\n" + "2. Most points " + name.title() + " scored in a season" + "\n"
                               + "3. Update the first name of " + name.title()
                               + "\n4. What teams did " + name.title() + " play for" + "\nEnter selection here: "))
        if second_message < 1 or second_message > 4:
            print("Please type a number between 1 and 4 inclusive. Try again")
    except ValueError:   # catches error if user enters nothing
        print("Please type a number between 1 and 4 inclusive. Try again")
    else:
        if second_message == 1:
            other_cursor.execute("select seasons_stats.Year from seasons_stats where player = \'" + name + "\'")
            print("Years:", end=" ")
            for row in other_cursor:
                print(str(*row) + " ", end=" ")
        elif (second_message == 2):

            other_cursor.execute("select seasons_stats.pts from seasons_stats where player = \'" + name + "\'")
            for row in other_cursor:
                integer = str(*row)  # a tuble cannot be converted to a int but can with string so i covert it to string and then to int with int() function
                if (int(integer) > my_points):
                    my_points = int(integer)
            print("Most points in a season by " + name.title() + ": " + str(my_points))
        elif (second_message == 3):
            updated_name = input("The name you want to update with " + name.title() + ":") + " " + message_list[1]

            other_cursor.execute("update seasons_stats set player = \'" + updated_name + "\'" + " where player = \'" + name + "\'")
            print("UPDATED!!! The new name is: " + updated_name.title())
        elif (second_message == 4):

            other_cursor.execute("select seasons_stats.tm from seasons_stats where player = \'" + name + "\'")
            for row in other_cursor:
                if (line_count == 0):
                    team_list.append(str(*row))
                else:
                    if str(*row) not in team_list:
                        team_list.append(str(*row))
                line_count += 1
            print("The team(s) " + name + " has played for are/is:")
            for team in team_list:
                print(team + " \n", end="", )
        try:
            final_message = int(input("\n" + "If you would like to access another player, ENTER 1. If you would like to quit, ENTER 2. If you would like to continue with same player"
               ", ENTER any different number than 1 and 2:"))
        except (ValueError, UnboundLocalError):
            print("Please type a number. Try again")
        else:
            if (final_message == 1):
                return 0
            elif (final_message == 2):
                return 1
            else:
                temp_function(message)


while quit == 0:
    try:
        message = str(input("\nPlease provide full name of the player you would like to access: "))
        message_list = message.split()
        mycursor.execute("select *  from seasons_stats where player = \'" + message + "\'")
        row = mycursor.fetchone()  # this and the if below basically checks if the user inputted a name that exists
        if row is None:
            print("Looks like that name does not exist in database! Please try again.")
            continue

    except mysql.connector.DatabaseError as er:  # if the name does not exit it catches and prints out the error message below
        print("Looks like that name does not exist in database! Please try again: {}".format(er))
    else:
       quit = temp_function(message)
