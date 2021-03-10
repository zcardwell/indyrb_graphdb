import numpy as np
import neo4j 

all_availabilities = ['first','second','third']
roles = ['manager','service clerk','office clerk','cashier']


def generate_people(number_of_people,seed = 314):
    hex_codes = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e']
    persons = []
    R = np.random.RandomState(seed)

    for i in range(number_of_people):
        
        person_id = ''.join(R.choice(hex_codes,size = 24))
        role = R.choice(roles)
        availability = R.choice(all_availabilities)
        age = R.randint(low = 16, high = 65)
        role_tenure = R.randint(low = 1, high = 10)
        p = {'name':person_id,'role':role,'age':age,'role_tenure':role_tenure,'availability':availability}
        persons.append(p)

    return persons



def ingest(persons,driver):

    for person in persons:

        #create person node

        create_person = f"""
        CREATE (p:person {{name:'{person['name']}',age:{person['age']}}})
        RETURN p
        """

        #create role node and relationship to person
        ##Using Merge incase it exists
        create_role = f"""
        MERGE (r:role {{name:'{person['role']}'}})
        MERGE (p:person {{name:'{person['name']}'}})
        MERGE (p)-[l:HAS_ROLE {{tenure:{person['role_tenure']}}}]->(r)
        RETURN p,l,r
        """

        #create availability node and relationship to person 

        create_availability = f"""
        MERGE (a:availability {{name:'{person['availability']}'}})
        MERGE (p:person {{name:'{person['name']}'}})
        MERGE (p)-[l:HAS_AVAILABILITY]->(a)
        RETURN p,l,a
        """

        with driver.session() as session:

            session.run(create_person)
            session.run(create_role)
            session.run(create_availability)


if __name__ == "__main__":

    #driver creation
    g = neo4j.GraphDatabase()
    driver = g.driver(uri=f"neo4j://localhost:7687",
                  auth=("neo4j", '1234'))

    #graph ingestion
    persons = generate_people(100)
    ingest(persons,driver)




