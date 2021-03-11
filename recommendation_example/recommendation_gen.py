import numpy as np
import neo4j



event_types = ['pop','jazz','country','classical','hip hop', 'rap','rock']

##This is Docker Code for Naming
left = ["admiring","adoring","affectionate","agitated","amazing","angry","awesome","beautiful","blissful","bold","boring","brave","busy","charming","clever","cool","compassionate","competent","condescending","confident","cranky","crazy","dazzling","determined","distracted","dreamy","eager","ecstatic","elastic","elated","elegant","eloquent","epic","exciting","fervent","festive","flamboyant","focused","friendly","frosty","funny","gallant","gifted","goofy","gracious","great","happy","hardcore","heuristic","hopeful","hungry","infallible","inspiring","interesting","intelligent","jolly","jovial","keen","kind","laughing","loving","lucid","magical","mystifying","modest","musing","naughty","nervous","nice","nifty","nostalgic","objective","optimistic","peaceful","pedantic","pensive","practical","priceless","quirky","quizzical","recursing","relaxed","reverent","romantic","sad","serene","sharp","silly","sleepy","stoic","strange","stupefied","suspicious","sweet","tender","thirsty","trusting","unruffled","upbeat","vibrant","vigilant","vigorous","wizardly","wonderful","xenodochial","youthful","zealous","zen"]
right = ["albattani","allen","almeida","antonelli","agnesi","archimedes","ardinghelli","aryabhata","austin","babbage","banach","banzai","bardeen","bartik","bassi","beaver","bell","benz","bhabha","bhaskara","black","blackburn","blackwell","bohr","booth","borg","bose","bouman","boyd","brahmagupta","brattain","brown","buck","burnell","cannon","carson","cartwright","carver","cerf","chandrasekhar","chaplygin","chatelet","chatterjee","chebyshev","cohen","chaum","clarke","colden","cori","cray","curran","curie","darwin","davinci","dewdney","dhawan","diffie","dijkstra","dirac","driscoll","dubinsky","easley","edison","einstein","elbakyan","elgamal","elion","ellis","engelbart","euclid","euler","faraday","feistel","fermat","fermi","feynman","franklin","gagarin","galileo","galois","ganguly","gates","gauss","germain","goldberg","goldstine","goldwasser","golick","goodall","gould","greider","grothendieck","haibt","hamilton","haslett","hawking","hellman","heisenberg","hermann","herschel","hertz","heyrovsky","hodgkin","hofstadter","hoover","hopper","hugle","hypatia","ishizaka","jackson","jang","jemison","jennings","jepsen","johnson","joliot","jones","kalam","kapitsa","kare","keldysh","keller","kepler","khayyam","khorana","kilby","kirch","knuth","kowalevski","lalande","lamarr","lamport","leakey","leavitt","lederberg","lehmann","lewin","lichterman","liskov","lovelace","lumiere","mahavira","margulis","matsumoto","maxwell","mayer","mccarthy","mcclintock","mclaren","mclean","mcnulty","mendel","mendeleev","meitner","meninsky","merkle","mestorf","mirzakhani","moore","morse","murdock","moser","napier","nash","neumann","newton","nightingale","nobel","noether","northcutt","noyce","panini","pare","pascal","pasteur","payne","perlman","pike","poincare","poitras","proskuriakova","ptolemy","raman","ramanujan","ride","montalcini","ritchie","rhodes","robinson","roentgen","rosalind","rubin","saha","sammet","sanderson","satoshi","shamir","shannon","shaw","shirley","shockley","shtern","sinoussi","snyder","solomon","spence","stonebraker","sutherland","swanson","swartz","swirles","taussig","tereshkova","tesla","tharp","thompson","torvalds","tu","turing","varahamihira","vaughan","visvesvaraya","volhard","villani","wescoff","wilbur","wiles","williams","williamson","wilson","wing","wozniak","wright","wu","yalow","yonath","zhukovsky"]

def generate_hidden_preferences(number_of_people,seed = 314):
    hex_codes = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e']
    persons = []
    R = np.random.RandomState(seed)

    for i in range(number_of_people):
        
        person_id = ''.join(R.choice(hex_codes,size = 24))
        person = {'name':person_id}
        for et in event_types:
            person[et] = R.uniform()

        persons.append(person)


    return persons

def generate_acts(number_of_acts,seed = 272):
    R = np.random.RandomState(seed)
    acts = []
    for i in range(number_of_acts):
        act_name = ' '.join([R.choice(left),R.choice(right)])
        assigned_event = R.choice(event_types)
        act = {'name':act_name, 'event_type':assigned_event}
        acts.append(act)

    return acts


def generate_likes(persons,acts, seed = 124):

    R = np.random.RandomState(seed)
    likes = []
    for person in persons:
        like = {'name':person['name'],'likes':[],'dislikes':[]}

        known_acts = (acts[i] for i in R.randint(low = 0, high = len(acts),size = R.randint(low = 1, high = 20)))

        for act in known_acts:
            et = act['event_type']
            act_name = act['name']
            coin_flip = R.uniform()
            score_to_beat = person[et]
            if coin_flip >= score_to_beat:
                like['likes'].append(act_name)
            else:
                like['dislikes'].append(act_name)
        likes.append(like)

    return likes



def ingest_data(likes,acts,driver):

    #inserting the acts
    with driver.session() as session:
        for act in acts:
            #insert the act
            insert_act = f"""
            MERGE (a:act {{name:'{act['name']}'}})
            MERGE (g:genre {{name:'{act['event_type']}'}})
            MERGE (g)<-[l:IN_GENRE]-(a)
            RETURN a,l,g
            """
            session.run(insert_act)

    #inserting the likes and dislikes
    print(likes)
    for person in likes:
        person_name = person['name']
        with driver.session() as session:

            for like in person['likes']:
                insert_like = f"""
                MERGE (p:person {{name:'{person_name}'}})
                MERGE (a:act {{name:'{like}'}})
                MERGE (p)-[l:RATED {{score: 1}}]->(a)
                RETURN p,a,l
                """
                session.run(insert_like)
            for dislike in person['dislikes']:
                insert_dislike = f"""
                MERGE (p:person {{name:'{person_name}'}})
                MERGE (a:act {{name:'{dislike}'}})
                MERGE (p)-[l:RATED {{score: -1}}]->(a)
                RETURN p,a,l
                """
                session.run(insert_dislike)

if __name__ == "__main__":
    g = neo4j.GraphDatabase()
    driver = g.driver(uri=f"neo4j://localhost:7687",
                  auth=("neo4j", '1234'))

    prefs = generate_hidden_preferences(1000)
    acts = generate_acts(100)
    likes = generate_likes(prefs,acts)
    ingest_data(likes,acts,driver)









