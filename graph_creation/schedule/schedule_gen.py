import numpy as np 




for person in persons:

    #create person node

    create_person = f"""
    CREATE (p:person {{name:{person['name']},age:{person['age']}}})
    RETURN p
    """

    #create role node and relationship to person
    ##Using Merge incase it exists
    create_role = f"""
    MERGE (r:role {{name:{person['role']}}})
    MATCH (p:person {{name:{person['name']}}})
    MERGE (p)-[l:HAS_ROLE {{tenure:{person['role_tenure']}}}]->(r)
    RETURN p,l,r
    """

    #create availability node and relationship to person 

    create_availability = f"""
    MERGE (a:availability {{name:{person['availability']}}})
    MATCH (p:person {{name:{person['name']}}})
    MERGE (p)-[l:HAS_AVAILABILITY]->(a)
    RETURN p,l,r
    """

