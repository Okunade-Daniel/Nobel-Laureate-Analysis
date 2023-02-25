#Reading in the data
df = pd.read_csv(r'C:\Users\DELL\Desktop\dataset\new datasets\nobel laurette\complete.csv')
print(df.shape)

#Limits the df to only individuals
#df = df[df['laureate_type']=='Individual']

#drop columns not needed for the analysis
df.drop(['categoryFullName','sortOrder','portion','prizeAmount','dateAwarded','categoryTopMotivation','award_link','knownName','givenName','familyName','fullName','penName'],axis='columns',inplace=True)
df.drop(['laureate_link','birth_city','birth_country','birth_locationString','death_date','death_city','death_cityNow','death_countryNow','death_continent','death_country','death_locationString',],axis='columns',inplace=True)
df.drop(['nativeName','acronym','org_founded_date','org_founded_city','org_founded_country','org_founded_locationString','residence_1','residence_2','affiliation_1','affiliation_2','affiliation_3','affiliation_4'],axis='columns',inplace=True)

df.columns = ['year','category','prize_value','prize_status','motivation','laureate_id', 'name','gender','birth_date','birth_city','birth_continent','birth_country','organisation_name','organisation_city','organisation_continent','organisation_country','laureate_type']

#Clean the category column
df['category'] = df['category'].replace({'Economic Sciences':'Economics', 'Physiology or Medicine':'Medicine'})

#Add a decade column to the dataset
df['decade'] = (np.floor(df.year/ 10) * 10).astype(int)

#Cnanging datatypes and adding the year of birth column
df['category'] = df.category.astype('category')
df['prize_status'] =df.prize_status.astype('category')
df['motivation'] = df.motivation.astype('string')
df['name'] = df.name.astype('string')
df['year of birth'] = df['birth_date'].str.extract(r'(^\d+)-', expand=False)
df['gender'] =df.gender.astype('category')
df['birth_city'] = df.birth_city.astype('string')
df['birth_continent'] = df.birth_continent.astype('category')
df['birth_country'] = df.birth_country.astype('string')
df['organisation_name'] = df.organisation_name.astype('string')
df['organisation_city'] = df.organisation_name.astype('string')
df['organisation_continent'] = df.organisation_continent.astype('category')
df['organisation_country'] = df.organisation_country.astype('string')
df['laureate_type'] = df.laureate_type.astype('category')
df['age'] = df['year'] - df['year of birth'].astype('float')

df.drop('birth_date', inplace=True, axis = 'columns')

#min age by gender
age = df.groupby('gender').agg({'age':'min'}).reset_index()
col = ['gold' if g == age['age'].min() else 'grey' for g in age['age']]  

#multiple winners
multiple_winners = df[df['name'].duplicated(keep='first')]
multiple_winners =multiple_winners.groupby('gender')['laureate_id'].count().reset_index()

#men status
men = df[df['gender']=='male']
men_dough =  men.groupby('category').agg({'gender':'count'}).reset_index()
men_dough.columns = ['category', 'no_winners']

#women status
women = df[df['gender']=='female']
women_dough =  women.groupby('category').agg({'gender':'count'}).reset_index()
women_dough.columns = ['category', 'no_winners']
 
c1 = np.array(['gold' if c == women_dough['no_winners'].max() else 'grey' for c in women_dough['no_winners']])
c2 = np.array(['gold' if c == men_dough['no_winners'].max() else 'grey' for c in men_dough['no_winners']])


#men continents
men_cont = men.groupby('birth_continent').agg({'category':'count'}).reset_index()
men_cont.columns = ['continent', 'no_winners']
men_cont = men_cont.sort_values(by='no_winners', ascending=True)
#women continents
women_cont = women.groupby('birth_continent').agg({'category':'count'}).reset_index()
women_cont.columns = ['continent', 'no_winners']
women_cont = women_cont.sort_values(by='no_winners', ascending=True)

co1 = np.array(['gold' if c == men_cont['no_winners'].max() else 'grey' for c in men_cont['no_winners']])
co2 = np.array(['gold' if c == women_cont['no_winners'].max() else 'grey' for c in women_cont['no_winners']])

#Limit the dataframe to only include award given to individuals alone
df = df[df['laureate_type']=='Individual']
