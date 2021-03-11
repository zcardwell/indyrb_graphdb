MATCH (n:person) RETURN n LIMIT 1
//
MATCH path = (n:person) -[r:RATED]->(a:act)-[l:IN_GENRE]->(g:genre)
WHERE n.name = '8d936ae072a86703c67840b4'
RETURN path
//
MATCH path = (n:person) -[r:RATED]->(a:act)-[l:IN_GENRE]->(g:genre)
WHERE n.name = '8d936ae072a86703c67840b4'
RETURN n.name as name,g.name as genre, sum(r.score) as score 
ORDER BY score DESC
//
MATCH path = (n:person) -[r1:RATED]->(a:act)<-[r2:RATED]-(n2:person)-[r3:RATED]->(a2:act)-[:IN_GENRE]->(g:genre)
WHERE n.name = '8d936ae072a86703c67840b4'
AND r1.score > 0 AND r2.score > 0 AND NOT a.name = a2.name
RETURN n.name as name, a2.name as suggested_act, sum(r3.score) as total_score , g.name as genre
ORDER BY total_score desc
//
MATCH (g:genre)<-[]-(a:act)<-[r:RATED]-(p:person)-[r2:RATED]->(a2:act)-[]->(g2:genre)
WHERE a.name = "exciting maxwell"
RETURN a.name as my_act,g.name as my_genre,a2.name as associated_act, g2.name as associated_genre,sum(r.score + r2.score) as combo_score
ORDER BY combo_score DESC
//
MATCH (g:genre)<-[]-(a:act)<-[r:RATED]-(p:person)-[r2:RATED]->(a2:act)-[]->(g2:genre)
WHERE a.name = "exciting maxwell"
RETURN a.name as my_act,g.name as my_genre, g2.name as associated_genre,sum(r.score + r2.score) as combo_score
ORDER BY combo_score DESC
//
MATCH (p1:person)-[r1:RATED]->(a:act)<-[r2:RATED]-(p2:person)
WHERE p1.name =  '8d936ae072a86703c67840b4'
RETURN p1.name as my_name, p2.name as other_person_name, 0.5*avg(r1.score + r2.score) as similarity_score
ORDER BY similarity_score DESC