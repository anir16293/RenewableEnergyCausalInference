
from data_analysis import SqlConnection

host = 'database-1.cftlk3722yhu.us-east-1.rds.amazonaws.com'
user = 'admin'
port = 3306
db = 'project_db'
password = '$kybluejays'

sql_connection = SqlConnection(host=host, user = user, port = port, db = db, password = password)

country_list = ["Zimbabwe", "Zambia", "Yemen, Rep.", "World", "West Bank and Gaza", "Virgin Islands (U.S.)", "Vietnam", "Venezuela, RB",
"Vanuatu", "Uzbekistan", "Uruguay", "Upper middle income", "United States", "United Kingdom", "United Arab Emirates",
"Ukraine", "Uganda", "Tuvalu", "Turks and Caicos Islands", "Turkmenistan", "Turkey", "Tunisia", "Trinidad and Tobago",
"Tonga", "Togo", "Timor-Leste", "Thailand", "Tanzania", "Tajikistan", "Syrian Arab Republic", "Switzerland", "Sweden",
"Suriname", "Sudan", "Sub-Saharan Africa (IDA & IBRD countries)", "Sub-Saharan Africa (excluding high income)", "Sub-Saharan Africa",
"St. Vincent and the Grenadines", "St. Martin (French part)", "St. Lucia", "St. Kitts and Nevis", "Sri Lanka",
"Spain", "South Sudan", "South Asia (IDA & IBRD)", "South Asia", "South Africa", "Somalia", "Solomon Islands", "Small states", "Slovenia", "Slovak Republic", "Sint Maarten (Dutch part)", "Singapore", "Sierra Leone", "Seychelles", "Serbia",
"Senegal", "Saudi Arabia", "Sao Tome and Principe", "San Marino", "Samoa", "Rwanda", "Russian Federation", "Romania",
"Qatar", "Puerto Rico", "Pre-demographic dividend", "Post-demographic dividend", "Portugal", "Poland", "Philippines",
"Peru", "Paraguay", "Papua New Guinea", "Panama", "Palau", "Pakistan", "Pacific island small states", "Other small states",
"Oman", "OECD members", "Not classified", "Norway", "Northern Mariana Islands", "North Macedonia", "North America",
"Nigeria", "Niger", "Nicaragua", "New Zealand", "New Caledonia", "Netherlands", "Nepal", "Nauru", "Namibia", "Myanmar",
"Mozambique", "Morocco", "Montenegro", "Mongolia", "Monaco", "Moldova", "Middle income", "Middle East & North Africa (IDA & IBRD countries)",
"Middle East & North Africa (excluding high income)", "Middle East & North Africa", "Micronesia, Fed. Sts.", "Mexico", "Mauritius", "Mauritania", "Marshall Islands", "Malta", "Mali", "Maldives", "Malaysia", "Malawi",
"Madagascar", "Macao SAR, China", "Luxembourg", "Lower middle income", "Low income", "Low & middle income", "Lithuania",
"Liechtenstein", "Libya", "Liberia", "Lesotho", "Lebanon", "Least developed countries: UN classification", "Latvia", "Latin America & the Caribbean (IDA & IBRD countrie",
"Latin America & Caribbean (excluding high income)", "Latin America & Caribbean", "Late-demographic dividend", "Lao PDR",
"Kyrgyz Republic", "Kuwait", "Kosovo", "Korea, Rep.", "Korea, Dem. People’s Rep.", "Kiribati", "Kenya", "Kazakhstan",
"Jordan", "Japan", "Jamaica", "Italy", "Israel", "Isle of Man",
"Ireland", "Iraq", "Iran, Islamic Rep.", "Indonesia", "India", "IDA total", "IDA only", "IDA blend", "IDA & IBRD total",
"Iceland", "IBRD only", "Hungary", "Hong Kong SAR, China", "Honduras", "High income", "Heavily indebted poor countries (HIPC)",
"Haiti", "Guyana", "Guinea-Bissau", "Guinea", "Guatemala", "Guam", "Grenada", "Greenland", "Greece", "Gibraltar", "Ghana",
"Germany", "Georgia", "Gambia, The", "Gabon", "French Polynesia", "France", "Fragile and conflict affected situations",
"Finland", "Fiji", "Faroe Islands", "European Union", "Europe & Central Asia (IDA & IBRD countries)", "Europe & Central Asia (excluding high income)", "Europe & Central Asia", "Euro area", "Ethiopia", "Eswatini", "Estonia", "Eritrea", "Equatorial Guinea",
"El Salvador", "Egypt, Arab Rep.", "Ecuador", "East Asia & Pacific (IDA & IBRD countries)", "East Asia & Pacific (excluding high income)",
"East Asia & Pacific", "Early-demographic dividend", "Dominican Republic", "Dominica", "Djibouti", "Denmark", "Czech Republic",
"Cyprus", "Curacao", "Cuba", "Croatia", "Cote d\'Ivoire", "Costa Rica", "Congo, Rep.", "Congo, Dem. Rep.", "Comoros",
"Colombia", "China", "Chile", "Channel Islands", "Chad", "Central Europe and the Baltics", "Central African Republic",
"Cayman Islands", "Caribbean small states", "Canada", "Cameroon", "Cambodia", "Cabo Verde", "Burundi", "Burkina Faso",
"Bulgaria", "Brunei Darussalam", "British Virgin Islands", "Brazil", "Botswana", "Bosnia and Herzegovina", "Bolivia",
"Bhutan", "Bermuda", "Benin", "Belize", "Belgium", "Belarus", "Barbados", "Bangladesh", "Bahrain", "Bahamas, The",
"Azerbaijan", "Austria", "Australia", "Aruba", "Armenia", "Argentina", "Arab World", "Antigua and Barbuda", "Angola",
"Andorra", "American Samoa", "Algeria", "Albania", "Afghanistan"]
year_list =  ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970',
              '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981',
              '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992',
              '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
              '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
              '2015', '2016', '2017']
resource_list = ["coal","nuclear","oil","renewable"]
hdi_list = {"happiness score":"happiness_score", "government corruption score": "government_corruption" , "life expectancy":"life_expectancy"}

def nli_func(str = ""):
    # hdi_idx
    if not str:
        str = "what is the happiness score of zimbabwe"
        str = "what is zimbabwe 's government corruption score"
        str = "how much is the life expectancy of australia"
        str = "give the happiness score of united states"


        #percentage_elec_from_source_idx
        str = "what is the percentage of electricity generated from nuclear resources in australia in 1980"
        str = "what percentage of electricity generated in australia in 1980 is from coal"
        str = "in 1980 in australia what is the percentage of electricity generated from oil"



        # per_capita_idx
        str = "what is the per capita consumption of oil to produce electricity in zimbabwe in 1980"
        str = "how much oil is consumed per capita to produce electricity in australia in 1980"

        #correlation_idx
        str = "what is the correlation between the oil of australia to 2000 from 1990 and coal of china"
        str = "between the oil of australia from the years 1990 to 2000 and the coal of china what is the correlation "


    per_capita_idx = str.find("per capita")
    percentage_elec_from_source_idx = str.find("percentage of electricity")
    hdi_idx = max(str.find("happiness score"),str.find("government corruption score"),str.find("life expectancy"))
    correlation_idx = str.find("correlation")

    if per_capita_idx > -1:
        country = None
        year = None

        str = str.lower()
        for elem in country_list:
            country_idx = str.find(elem.lower())
            if country_idx > -1:
                country = elem
                break
        for elem in year_list:
            year_idx = str.find(elem.lower())
            if year_idx > -1:
                year = elem
                break
        sql = "SELECT kg FROM project_db.electricity_per_capita INNER JOIN project_db.country_code ON country_code.country_code = electricity_per_capita.country_code WHERE country_code.country_name = \"xxCountryxx\" AND year = xxyearxx ; "
        sql = sql.replace("xxCountryxx", country)
        sql = sql.replace("xxyearxx", year)
        # print(sql)
        return('The electricity per capita for {} in {} is {}'.format(country, year, sql_connection.execute_sql(sql)[0,0]))
    elif  percentage_elec_from_source_idx > -1:
        country = None
        year = None
        resource = None

        str = str.lower()
        for elem in country_list:
            country_idx = str.find(elem.lower())
            if country_idx > -1:
                country = elem
                break

        for elem in year_list:
            year_idx = str.find(elem.lower())
            if year_idx > -1:
                year = elem
                break

        for elem in resource_list:
            resource_idx = str.find(elem.lower())
            if resource_idx > -1:
                resource = elem
                break
        sql = "SELECT percentage FROM project_db.electricity_from_xxresourcexx_percentage INNER JOIN project_db.country_code ON country_code.country_code = electricity_from_xxresourcexx_percentage.country_code WHERE country_code.country_name = \"xxCountryxx\" AND year = xxyearxx ; "
        sql = sql.replace("xxCountryxx", country)
        sql = sql.replace("xxyearxx", year)
        sql = sql.replace("xxresourcexx", resource)
        print(sql)
        return sql_connection.execute_sql(sql)

    elif hdi_idx > -1:
        country = None
        hdi = None

        str = str.lower()
        for elem in country_list:
            country_idx = str.find(elem.lower())
            if country_idx > -1:
                country = elem
                break

        for elem in hdi_list:
            hdi_idx = str.find(elem.lower())
            if hdi_idx > -1:
                hdi = elem
                break
        sql = "SELECT xxhdi_entityxx FROM project_db.world_happiness_index where country = \"xxCountryxx\" ;"
        sql = sql.replace("xxhdi_entityxx", hdi_list[hdi])
        sql = sql.replace("xxCountryxx", country)
        print(sql)
        return sql_connection.execute_sql(sql)

    elif correlation_idx > -1 :
        country_1= None
        country_1_idx = -1
        country_2= None
        country_2_idx = -1
        year_1 = None
        year_2 = None
        resource_1 = None
        resource_1_idx = None
        resource_2 = None
        resource_2_idx = None

        str = str.lower()
        for elem in country_list:
            country_idx = str.find(elem.lower())
            if country_idx > -1:
                if not country_1:
                    country_1_idx = country_idx
                    country_1 = elem
                elif not country_2:
                    country_2_idx = country_idx
                    country_2 = elem

        for elem in year_list:
            year_idx = str.find(elem.lower())
            if year_idx > -1:
                if not year_1:
                    year_1 = elem
                else:
                    if elem < year_1:
                        year_2 = year_1
                        year_1 = elem
                    else:
                        year_2 = elem

        for elem in resource_list:
            resource_idx = str.find(elem.lower())
            if resource_idx > -1:
                if not resource_1:
                    resource_1 = elem
                    resource_1_idx = resource_idx
                elif not resource_2:
                    resource_2 = elem
                    resource_2_idx = resource_idx

        if abs(country_1_idx - resource_1_idx) > abs(country_1_idx - resource_2_idx):
            temp = resource_2
            resource_2 = resource_1
            resource_1 = temp

        sql1 = "CREATE VIEW country1_resource1 AS SELECT DISTINCT year, percentage FROM electricity_from_xxresource1xx_percentage as e, country_code as c WHERE e.country_code = c.country_code AND c.country_name = \"xxcountry1xx\" AND year <= xxyear2xx AND year >= xxyear1xx ;"

        sql1 = sql1.replace("xxcountry1xx",country_1)
        sql1 = sql1.replace("xxyear2xx",year_2)
        sql1 = sql1.replace("xxyear1xx",year_1)
        sql1 = sql1.replace("xxresource1xx",resource_1)

        sql2 = "CREATE VIEW country2_resource2 AS SELECT DISTINCT year, percentage FROM electricity_from_xxresource2xx_percentage as e, country_code as c WHERE e.country_code = c.country_code AND c.country_name = \"xxcountry2xx\" AND year <= xxyear2xx AND year >= xxyear1xx ;"

        sql2 = sql2.replace("xxcountry2xx", country_2)
        sql2 = sql2.replace("xxyear2xx", year_2)
        sql2 = sql2.replace("xxyear1xx", year_1)
        sql2 = sql2.replace("xxresource2xx", resource_2)

        sql3 = "SELECT AVG((s.percentage - (SELECT AVG(s.percentage) FROM country1_resource1 s))*(i.percentage - (SELECT AVG(i.percentage) FROM country2_resource2 i)))/((SELECT STDDEV(s1.percentage) from country1_resource1 s1)*(SELECT STDDEV(s2.percentage) FROM country2_resource2 s2)) FROM country1_resource1 as s, country2_resource2 as i WHERE s.year = i.year;"

        sql4 = "drop view if exists country1_resource1, country2_resource2;"
        # print(sql4+sql1+sql2+sql3+sql4)
        # _ = sql_connection.execute_sql(sql4)
        _ = sql_connection.execute_sql(sql1)
        _ = sql_connection.execute_sql(sql2)
        res = sql_connection.execute_sql(sql3)
        _ = sql_connection.execute_sql(sql4)
        return res

    else:
        return "Error: Please try rephrasing input sentence "



if __name__ == '__main__':
    sql = nli_func('How much is the per capita consumption of coal to produce electricity in Australia in 2010?')
    print(sql)

    sql = nli_func('What is the correlation between the oil of australia to 2000 from 1990 and coal of china?')
    print(sql)
