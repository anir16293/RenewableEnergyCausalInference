import matplotlib.pyplot as plt
import numpy as np
from data_analysis import SqlConnection

def main():
    happiness_sql = 'SELECT happiness_score, e.percentage FROM world_happiness_index, electricity_from_renewable_percentage e, country_code c where c.country_name = country AND c.country_code = e.country_code AND year = 2015;'
    life_sql = 'SELECT life_expectancy, e.percentage FROM world_happiness_index, electricity_from_renewable_percentage e, country_code c where c.country_name = country AND c.country_code = e.country_code AND year = 2015;'
    life_lower_mid_income_sql = 'SELECT life_expectancy, e.percentage FROM world_happiness_index, electricity_from_renewable_percentage e, country_code c, country_metadata m where c.country_name = country AND c.country_code = e.country_code AND year = 2015 AND m.country_code = c.country_code AND m.IncomeGroup = "Lower middle Income";'
    happiness_lower_mid_income_sql = 'SELECT happiness_score, e.percentage FROM world_happiness_index, electricity_from_renewable_percentage e, country_code c, country_metadata m where c.country_name = country AND c.country_code = e.country_code AND year = 2015 AND m.country_code = c.country_code AND m.IncomeGroup = "Lower middle Income";'

    host = 'database-1.cftlk3722yhu.us-east-1.rds.amazonaws.com'
    user = 'admin'
    port = 3306
    db = 'project_db'
    password = '$kybluejays'

    connection = SqlConnection(host=host, user = user, port = port, db = db, password = password)

    array1 = connection.execute_sql(sql=happiness_sql)
    array2 = connection.execute_sql(sql=life_sql)
    array3 = connection.execute_sql(sql=life_lower_mid_income_sql)
    array4 = connection.execute_sql(sql=happiness_lower_mid_income_sql)


    plt.plot(array1[:,0], array1[:, 1],  'o')
    plt.title('Happiness score with percentage renewable consumption')
    plt.show()

    plt.plot(array2[:,0], array2[:, 1],  'o')
    plt.title('Life expectancy with percentage renewable consumption')
    plt.show()

    plt.plot(array3[:,0], array3[:, 1],  'o')
    plt.title('Life expectancy with renewable for lower middle income countries.')
    plt.show()

    plt.plot(array4[:,0], array4[:, 1],  'o')
    plt.title('Happiness with percentage renewable consumption for lower middle income countries.')
    plt.show()

if __name__ == '__main__':
    main()