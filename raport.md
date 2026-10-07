titanic_train

Ile rekordow i kolumn

RangeIndex: 891 entries, 0 to 890
Data columns (total 12 columns):

 #   Column       Non-Null Count  Dtype  
---  ------       --------------  -----  
 0   PassengerId  891 non-null    int64  
 1   Survived     891 non-null    int64  
 2   Pclass       891 non-null    int64  
 3   Name         891 non-null    str    
 4   Sex          891 non-null    str    
 5   Age          714 non-null    float64
 6   SibSp        891 non-null    int64  
 7   Parch        891 non-null    int64  
 8   Ticket       891 non-null    str    
 9   Fare         891 non-null    float64
 10  Cabin        204 non-null    str    
 11  Embarked     889 non-null    str   

Nawazniejsze zmienne w zbiorze
- Survived
- Pclass
- Sex

Jakie braki / problemy jakości danych zauważasz
- W kolumnie "Cabin" jest duzo brakow i to pole nie jest uzupelnione
- W kolumnie "Name" sa tez dane ktore nie powinny sie tam znajdowac



datasets_orders

Ile rekordow i kolumn

RangeIndex: 26552 entries, 0 to 26551
Data columns (total 7 columns):

 #   Column           Non-Null Count  Dtype  
---  ------           --------------  -----  
 0   order_date       26552 non-null  str    
 1   pages_visited    26552 non-null  int64  
 2   order_id         26552 non-null  str    
 3   customer_id      26552 non-null  str    
 4   tshirt_category  26552 non-null  str    
 5   tshirt_price     26552 non-null  float64
 6   tshirt_quantity  26552 non-null  int64  

Nawazniejsze zmienne w zbiorze
- tshirt_category
- tshirt_price
- tshirt_quantity

Jakie braki / problemy jakości danych zauważasz
- literowki w polach kolumny tshirt_category
- w polach kolumny tshirt_category sa potencjalne wartosci odstajace



Jak (na razie koncepcyjnie) można by później **polaczyc** te datasety w jednym pipeline Kedro (wspolny klucz? osobne galezie? ten sam schemat preprocessingu)?
- Zbiory danych titanic_test.csv oraz datasets_orders.csv reprezentuja calkowicie odmienne domeny biznesowe i nie posiadaja wspolnego klucza identyfikacyjnego
