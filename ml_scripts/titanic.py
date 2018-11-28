from sklearn.tree import DecisionTreeClassifier
from enum import Enum, unique
import pandas as pd
import numpy as np
import os


@unique
class Sex(Enum):
    male = 1
    female = 0


# Get data
df: pd.DataFrame = pd.DataFrame.from_csv(os.path.abspath(os.path.join('data', 'titanic.csv')))

select_columns: list = ['Pclass', 'Fare', 'Age', 'Sex']

filtered_df: pd.DataFrame = df[select_columns].copy(deep=True)
filtered_df['Sex'] = filtered_df['Sex'].apply(lambda x: Sex[x].value)
filtered_df.dropna(axis=0, inplace=True)
goal_variable = df['Survived'].copy(deep=True)
goal_variable = goal_variable.loc[filtered_df.index].values.reshape(-1, 1)

dtc = DecisionTreeClassifier(random_state=241)
dtc.fit(filtered_df.values, goal_variable)

importance = dtc.feature_importances_

# Find appropriate indexes
feature_with_first_imp_level_idx = None
feature_with_second_imp_level_idx = None

for i in range(0, np.alen(importance)):
    if feature_with_first_imp_level_idx is None:
        feature_with_first_imp_level_idx = i

    elif feature_with_second_imp_level_idx is None:
        feature_with_second_imp_level_idx = i

    else:
        first_val, second_val = importance[[feature_with_first_imp_level_idx, feature_with_second_imp_level_idx]]
        if first_val < second_val:
            feature_with_first_imp_level_idx, feature_with_second_imp_level_idx = feature_with_second_imp_level_idx, feature_with_first_imp_level_idx

        new_val = importance[i]

        if new_val > importance[feature_with_second_imp_level_idx]:
            feature_with_second_imp_level_idx = i

            first_val, second_val = importance[[feature_with_first_imp_level_idx, feature_with_second_imp_level_idx]]
            if first_val < second_val:
                feature_with_first_imp_level_idx, feature_with_second_imp_level_idx = feature_with_second_imp_level_idx, feature_with_first_imp_level_idx

feature_with_first_imp_level_name = select_columns[feature_with_first_imp_level_idx]
feature_with_second_imp_level_name = select_columns[feature_with_second_imp_level_idx]
