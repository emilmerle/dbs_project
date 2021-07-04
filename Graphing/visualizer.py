# psycopg2 wird importiert (muss installiert sein)
# Bibliothek, um sich mit PostgreSQL Datenbanken zu verbinden
import psycopg2
import matplotlib.pyplot as plt
import argparse



def get_data(country, identifier):
    attribute = ""
    if(identifier == "c"):
        attribute = "country_code"
        cur.execute(f"SELECT country_name FROM gdp WHERE country_code = '{country}'")
        name = cur.fetchone()[0]
    else:
        attribute = "country_name"
        name = country

    table = "gdp"
    query = f"SELECT * FROM {table} WHERE {attribute} = '{country}'"

    # get gdp values from given country
    cur.execute(query)
    gdp_result = list(cur.fetchone())[3:-1]

    table = "life_expectancy"
    query = f"SELECT * FROM {table} WHERE {attribute} = '{country}'"

    # get life_expectancy from given country
    cur.execute(query)
    le_result = list(cur.fetchone())[3:-1]

    return gdp_result, le_result, name

if __name__ == "__main__":

    # adding command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", type=str, help="Country code to get information about this country")
    parser.add_argument("--name", type=str, help="Country name to get information about this country")
    args = parser.parse_args()

    # exit if two arguments are given
    if (args.name and args.code):
        exit("Too many arguments given")

    if (not args.name and not args.code):
        exit("Too few arguments given")

    # Variablen werden definiert
    dbname = "dbs_project"
    username = "postgres"
    password = "emil"

    # Verbindung mit Datenbank als User mit Passwort wird hergestellt
    conn = psycopg2.connect(f"dbname={dbname} user={username} password={password}")

    # Cursor wird initialisiert um Abfragen entgegenzunehmen
    cur = conn.cursor()

    # check if given code or name exists
    cur.execute("SELECT country_code FROM gdp")
    codes = cur.fetchall()
    for i in range(len(codes)):
        codes[i]  = codes[i][0]

    cur.execute("SELECT country_name FROM gdp")
    names = cur.fetchall()
    for i in range(len(names)):
        names[i] = names[i][0]

    name = ""

    if(args.code):
        if(args.code not in codes):
            exit("Given country code not found")
        gdp, le, name = get_data(args.code, "c")

    if(args.name):
        if(args.name not in names):
            exit("Given country name not found")
        gdp, le, name = get_data(args.name, "n")


    # plotting:
    fig, ax = plt.subplots()

    ax.set_title(name)

    color = "tab:red"
    ax.set_xlabel("years")
    ax.set_ylabel("GDP", color=color)
    ax.plot([x for x in range(1960, 2016)], gdp, color=color)
    ax.tick_params(axis="y", labelcolor=color)

    ax2 = ax.twinx()

    color="tab:blue"

    ax2.set_ylabel("life expectancy", color=color)
    ax2.plot([x for x in range(1960, 2016)], le, color=color)
    ax2.tick_params(axis="y", labelcolor=color)
    
    plt.show()



    # Cursor und Verbindung zur Datenbank werden geschlossen
    cur.close()
    conn.close()