MATCH (n:availability) RETURN n LIMIT 25

//

MATCH (n:role) RETURN n LIMIT 25

//

MATCH (n:person) RETURN n LIMIT 25

//

match path = (a:availability)<-[:HAS_AVAILABILITY]-(p:person)-[:HAS_ROLE]->(r:role) return a.name as shift ,r.name as role, count(distinct p) as persons order by shift, role

//

create (s:shift)
set s.name = 'monday_shift'
return s

//

MATCH (a:availability {name:'first'})
with a
MATCH (s:shift {name:'monday_shift'})
with a,s
MERGE (s)-[ia:IN]->(a)
return s,ia,a

//

MATCH path = (s:shift)-[:IN]->(a:availability)<-[:HAS_AVAILABILITY]-(p:person)-[hr:HAS_ROLE]->(r:role)
where s.name = 'monday_shift'
return path

//
MATCH path = (s:shift)-[:IN]->(a:availability)<-[:HAS_AVAILABILITY]-(p:person)-[hr:HAS_ROLE]->(r:role)
where s.name = 'monday_shift' and not (p)-[:ASSIGNED]->(:shift)
with s as shift, r as role, max(hr.tenure) as max_tenure, a
MATCH (r)<-[hr:HAS_ROLE]-(p:person)-[:HAS_AVAILABILITY]->(a)
where hr.tenure = max_tenure and not (p)-[:ASSIGNED]->(:shift)
with r, collect(p)[0] as selected_persons, shift
MERGE (shift)<-[a:ASSIGNED]-(selected_persons)
return shift,a,selected_persons

//

create (s:shift)
set s.name = 'tuesday_shift'
return s

//

MATCH (a:availability {name:'first'})
with a
MATCH (s:shift {name:'tuesday_shift'})
with a,s
MERGE (s)-[ia:IN]->(a)
return s,ia,a

//
MATCH path = (s:shift)-[:IN]->(a:availability)<-[:HAS_AVAILABILITY]-(p:person)-[hr:HAS_ROLE]->(r:role)
where s.name = 'tuesday_shift' and not (p)-[:ASSIGNED]->(:shift)
with s as shift, r as role, max(hr.tenure) as max_tenure, a
MATCH (r)<-[hr:HAS_ROLE]-(p:person)-[:HAS_AVAILABILITY]->(a)
where hr.tenure = max_tenure and not (p)-[:ASSIGNED]->(:shift)
with r, collect(p)[0] as selected_persons, shift
MERGE (shift)<-[a:ASSIGNED]-(selected_persons)
return shift,a,selected_persons
