import torch
import torch.nn as nn
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import pymysql
from torch.utils.data import DataLoader
from typing import List, Tuple
import xgboost as xgb
import matplotlib.pyplot as plt

# Class definintion of the Neural Network to model Average Causal Effect (ACE)
class CausalRelationNetwork(nn.Module):
    def __init__(self, num_dimensions: int, num_hidden: int) -> None:
        super().__init__()
        self.linear1 = nn.Linear(num_dimensions, num_hidden)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(num_hidden, 64)
        self.linear3 = nn.Linear(64, 1)
        self.tanh = nn.Tanh()
        self.bn = nn.BatchNorm1d(num_features = 64)
        self.dropout = nn.Dropout(p = 0.2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.linear1(x)
        x = self.tanh(x)
        x = self.linear2(x)
        x = self.relu(x)
        # x = self.dropout(x)
        x = self.linear3(x)
        return(x)
    
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        return(self.forward(x))

# Class to obtain data directly from SQL using a Python cursor
class SqlDataset:
    # The SQL query must fetch the data s.t. the target variable is obtainable as the last dimension (-1).
    def __init__(self, sql_query: str):
        host = 'database-1.cftlk3722yhu.us-east-1.rds.amazonaws.com'
        user = 'admin'
        port = 3306
        db = 'project_db'
        password = '$kybluejays'
        self.connection = SqlConnection(host = host, user = user, port = port, db = db, password = password)
        self.data = self.connection.execute_sql(sql = sql_query)
    
    def __len__(self):
        return(self.data.shape[0])
    
    def __getitem__(self, idx):
        return((torch.tensor(self.data[idx, :-1], dtype = torch.float32), torch.tensor(self.data[idx, -1], dtype = torch.float32)))

# Function to train the Neural Network
def train_neural_network(model:nn.Module, dataset: SqlDataset, lr = 5*1e-4, num_epochs = 5000) -> None:
    optimizer = torch.optim.Adamax(params = model.parameters(), lr = lr)
    data = DataLoader(dataset = dataset, batch_size = 10, shuffle = False)
    loss_fn = nn.MSELoss()
    for epoch in range(num_epochs):
        running_loss = 0
        count = 0
        for X, y in data:
            optimizer.zero_grad()
            y_hat = model(X)
            loss = loss_fn(y_hat, y)
            loss.backward()
            optimizer.step()
            count += 1
            running_loss += loss.item()
        if epoch % 10 == 0:
            print('Epoch: {}, MSE Loss: {}'.format(epoch + 1, running_loss/count))

# Class definition of the Python to SQL connection class
class SqlConnection:
    def __init__(self, host:str, user:str, port:int, db: str, password: str) -> None:
        self.host = host
        self.user = user
        self.port = port
        self.db = db
        self.password = password

    def execute_sql(self, sql: str) -> Tuple[Tuple]:
        cn = pymysql.connect(host = self.host, user = self.user, password = self.password, port = self.port, db = self.db, cursorclass = pymysql.cursors.Cursor)
        with cn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        cn.close()
        return(np.array(result))

# Class definition of the class to model the causal relations
class CausalRelation:
    def __init__(self, sql_query: str, model: str = 'neural', is_mediation: bool = False, mediation_variable: int = -1) -> None:
        if model not in {'neural', 'random_forest', 'linear', 'gradient_boost'}:
            raise ValueError('Model name should be either neural, random_forest, linear')
        
        self.model_name = model

        if model in {'random_forest', 'linear', 'gradient_boost'}:
            host = 'database-1.cftlk3722yhu.us-east-1.rds.amazonaws.com'
            user = 'admin'
            port = 3306
            db = 'project_db'
            password = '$kybluejays'            
            connection = SqlConnection(host = host, user = user, port = port, db = db, password = password)
            res = connection.execute_sql(sql=sql_query)
            
            self.x = res[:, :-1]
            self.y = res[:, -1]

        if model == 'neural':
            dataset = SqlDataset(sql_query = sql_query)
            n_col = dataset.__getitem__(0)[0].size()[0]
            self.model = CausalRelationNetwork(num_dimensions = n_col, num_hidden = 128)
            print('Started training the neural network.')
            self.model = self.model.train()
            train_neural_network(model=self.model, dataset = dataset)
            self.model = self.model.eval()
            self.x = torch.tensor(dataset.data[:, :-1], dtype = torch.float32)
            self.y = torch.tensor(dataset.data[:, -1], dtype = torch.float32)

        elif model == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=1000)
            print('Fitting {} model to the given dataset.'.format(model))
            self.model.fit(self.x, self.y)
            # print(self.model.score(self.x, self.y))

        elif model == 'linear':
            print('Fitting {} model to the given dataset.'.format(model))
            self.model = LinearRegression()
            self.model.fit(self.x, self.y)
            # print(self.model.score(self.x, self.y))
        
        elif model == 'gradient_boost':
            print('Fitting {} model to the given dataset.'.format(model))
            self.model = xgb.XGBRegressor(objective = 'reg:squarederror')
            self.model.fit(self.x, self.y)
            # print(self.model.score(self.x, self.y))
        
        self.is_mediation = is_mediation
        self.mediaton_variable = mediation_variable
        if self.is_mediation:
            self.mediation_model = LinearRegression()
            self.mediation_model.fit(self.x[:, self.mediaton_variable].reshape(-1, 1), self.y)
            # print(self.mediation_model.score(self.x[:, self.mediaton_variable].reshape(-1, 1), self.y))

    def get_nace(self, treatment_dim: int, treatment_value: float) -> float:
        try:
            X_treatment = self.x.copy()
        except AttributeError:
            X_treatment = self.x.clone()
        X_treatment[:, treatment_dim] = treatment_value
        if self.is_mediation:
            adjusted_mediator_score = self.mediation_model.predict(np.array([treatment_value]).reshape(-1,1))[0]
            # print(adjusted_mediator_score)
            # print(X_treatment[:, self.mediaton_variable].mean())
            try:
                X_treatment[:, self.mediaton_variable] = np.array([adjusted_mediator_score]*X_treatment.shape[0])
            except TypeError:
                X_treatment[:, self.mediaton_variable] = torch.tensor([adjusted_mediator_score]*X_treatment.shape[0], dtype = torch.float32)
        nace = self.model.predict(X_treatment) - self.model.predict(self.x)
        mean_nace = []
        if self.model_name != 'neural':
            for _ in range(100):
                subset = np.random.choice(nace, size = 20)
                mean_nace.append(subset.mean())
        else:
            nace_numpy = nace.data.numpy().flatten()
            for _ in range(100):
                subset = np.random.choice(nace_numpy, size = 20)
                mean_nace.append(subset.mean())
        return(np.array(mean_nace).mean())

def main():
    happiness_sql_query = 'select o.percentage AS oil_percentage, r.percentage as renewable_percent, h.life_expectancy, h.government_corruption, h.happiness_score FROM electricity_from_oil_percentage o, electricity_from_renewable_percentage r, (select DISTINCT * FROM  world_happiness_index h INNER JOIN country_code c ON h.country = c.country_name) h WHERE o.year = r.year AND o.year = 2015 AND o.country_code = r.country_code AND o.country_code = h.country_code;'
    lower_mid_income_life_sql_query = 'select o.percentage AS oil_percentage, r.percentage as renewable_percent, h.government_corruption, h.life_expectancy, h.happiness_score FROM electricity_from_oil_percentage o, electricity_from_renewable_percentage r, (select DISTINCT * FROM  world_happiness_index h INNER JOIN country_code c ON h.country = c.country_name) h, country_metadata m WHERE o.year = r.year AND o.year = 2015 AND o.country_code = r.country_code AND o.country_code = h.country_code AND o.country_code = m.country_code AND m.IncomeGroup = "Lower Middle Income";'
    happiness_causal_inference = CausalRelation(sql_query=lower_mid_income_life_sql_query, model='linear')
    print('Linear model ACE {}'.format(happiness_causal_inference.get_nace(treatment_dim= 1, treatment_value = 50)))

    happiness_causal_inference = CausalRelation(sql_query=lower_mid_income_life_sql_query, model='neural')
    print('Neural Network ACE {}'.format(happiness_causal_inference.get_nace(treatment_dim= 1, treatment_value = 50)))

    happiness_causal_inference = CausalRelation(sql_query=lower_mid_income_life_sql_query, model='random_forest')
    print('Random Forest ACE {}'.format(happiness_causal_inference.get_nace(treatment_dim= 1, treatment_value = 50)))

    happiness_causal_inference = CausalRelation(sql_query=lower_mid_income_life_sql_query, model='gradient_boost')
    print('Gradient Boost ACE {}'.format(happiness_causal_inference.get_nace(treatment_dim= 1, treatment_value = 50)))

    life_sql_query = 'select o.percentage AS oil_percentage, r.percentage as renewable_percent, h.government_corruption, h.happiness_score,  h.life_expectancy FROM electricity_from_oil_percentage o, electricity_from_renewable_percentage r, (select DISTINCT * FROM  world_happiness_index h INNER JOIN country_code c ON h.country = c.country_name) h WHERE o.year = r.year AND o.year = 2015 AND o.country_code = r.country_code AND o.country_code = h.country_code;'
    life_causal_inference = CausalRelation(sql_query=life_sql_query, model='gradient_boost', is_mediation=True, mediation_variable=3)
    print('Model ACE {}'.format(life_causal_inference.get_nace(treatment_dim= 1, treatment_value = 50)))

    upper_mid_income_life_sql_query = 'select o.percentage AS oil_percentage, r.percentage as renewable_percent, h.government_corruption, h.happiness_score,  h.life_expectancy FROM electricity_from_oil_percentage o, electricity_from_renewable_percentage r, (select DISTINCT * FROM  world_happiness_index h INNER JOIN country_code c ON h.country = c.country_name) h, country_metadata m WHERE o.year = r.year AND o.year = 2015 AND o.country_code = r.country_code AND o.country_code = h.country_code AND o.country_code = m.country_code AND m.IncomeGroup = "Upper Middle Income";'
    life_causal_inference = CausalRelation(sql_query=upper_mid_income_life_sql_query, model='neural', is_mediation=True, mediation_variable=3)
    print('Model ACE {}'.format(life_causal_inference.get_nace(treatment_dim= 1, treatment_value = 80)))

if __name__ == '__main__':
    main()