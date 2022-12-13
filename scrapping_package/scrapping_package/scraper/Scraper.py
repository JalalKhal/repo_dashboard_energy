import asyncio
import aiohttp
import json
import validators  #validator of url
class Scraper:

    headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
             "Accept-Language":"fr;q=0.9",
             "Accept-Encoding":"gzip, deflate",
             "Accept":"text/html",
             "referer":"'https://www.google.com/'",
             } #headers of requests
    requests_per_unit=1 #numbers of asynchronous requests per unit time (cf time_wait)
    time_wait=10 #time to do a pause for requesting.
    file_name="output.json" #file name of requests content
    def __init__(self,urls,headers=headers,requests_per_unit=requests_per_unit,time_wait=time_wait,file_name=file_name):
        """
        :param urls: list of urls (list)
        :param headers: headers request (dictionnary)
        :param requests_per_unit: numbers of asynchronous requests per unit time (int>=0)
        :param time_wait: time (second) to wait for do a new requests_per_unit (float or int >=0)
        :param file_name: file name of file contains requests content (str)
        :param number_requests: number of requests (int)
        """
        self.urls=urls
        self.headers=headers
        self.requests_per_unit=requests_per_unit
        self.time_wait=time_wait
        self.file_name=file_name
        self.number_requests=len(self.urls)
        Scraper.verify_types(self)

    def verify_types(self):
        assert isinstance(self.urls,list)
        for url in self.urls:
            assert isinstance(url,str) #test if it's str
            assert validators.url(url) #test if it's url
        assert type(self.headers) is dict
        assert isinstance(self.requests_per_unit,int) and self.requests_per_unit>=0
        assert (isinstance(self.time_wait,float) or isinstance(self.time_wait,int)) and self.time_wait>=0
        assert isinstance(self.file_name,str)

    async def afetch(self,url,session):
        """
        :param url: url of website
        :param session: asynchronous session
        :return: fetch content of url from session
        """
        async with session.get(url,headers=self.headers) as response:
            return await response.read() #.read() return binary content

    async def agets(self,session,loop=asyncio.get_event_loop()): #coroutine
        """
            :param session: current session asynchronous of http resquests
            do asynchronous requests and set up into dictionnary ({"URL 0":content 0,"URL 1":content 1, ...})
        """
        tasks=[] #list of coroutines of all requests
        for i in range(self.number_requests):
            task=asyncio.create_task(self.afetch(self.urls[i],session)) #create task for urls[i]
            tasks.append(task)
            if self.time_wait > 0 and (i+1)% self.requests_per_unit ==0:
                await asyncio.sleep(self.time_wait)
        responses=await asyncio.gather(*tasks,return_exceptions=True) #gather: Return Future object :need to be awaited to get result (awaitable object)
                                                                        #gather: can take as parameter task or native co-routine.
        dict_responses={self.urls[i]:str(response) for i,response in enumerate(responses)} #.result() method from Future class
        return dict_responses

    async def awrite(self,session,mode="w"):
        """
        :param session: current session asynchronous of http resquests
        :param mode: writting mode: binary mode (wb) or writting mode (w)
        write results of requests into json file ({"URL 0":content 0,"URL 1":content 1 ...})
        """
        assert mode == "w" or mode == "wb" or mode == "a" or mode =="ab"
        dict_responses=await self.agets(session) #get the result of co-routine.
        with open(self.file_name,mode) as f:
            f.write(json.dumps(dict_responses,ensure_ascii=False)) #ensure_ascii=False to have non ascii character to unicode character


"""
gather et await: attende que la tache se finit
create_task + await: dans une asynchrounous function/method


difference asyncio.run() et asyncio.run_until_complete():


Application developers should typically use the high-level asyncio functions, such as asyncio.run(), 
and should rarely need to reference the loop object or call its methods. 
This section is intended mostly for authors of lower-level code, libraries, 
and frameworks, who need finer control over the event loop behavior.


Fonctions à exécuter qui ne sont pas asynchrones:
-->asyncio.run(): version amélioré qui met la co-routine dans la boucle puis l'execute
-->asyncio.run_until_complete(): version non amélioré:
avec asyncio.run():
    asyncio.run(main) avec main co-routines fonction/méthode (async def...) PAS Task object
avec asyncio.run_until_complete():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main)
    loop.close()
    ->explicitation de la boucle asyncio courante
    -->meme type que main ci-dessus (main co-routines fonction/méthode (async def...) PAS Task object)

3 types de variables:
co-routine: programme asynchrone native en python avec mot clé async (async def f()...)
Task: objet Task dans la bibiliothèque asyncio pour manipuler une co-routine, l'exécuter
Future: objet Futur qui contient le résultat éventuelle d'une co-routine (précisément d'une co-routines transformé en Task)

Ces 3 types sont de types awaitables c'est à dire qu'il faut utiliser le mot clé await variable pour pouvoir
attendre que l'execution se finisse du type de variable condiéré.
Rq: Future au niveau applicatif, on ne l'utilise pas normalement.
Futures
A Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation.
When a Future object is awaited it means that the coroutine will wait until the Future is resolved in some other place.

Groupe de tasks:
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(
            say_after(1, 'hello'))

        task2 = tg.create_task(
            say_after(2, 'world'))

        print(f"started at {time.strftime('%X')}")

    # The wait is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")
    
context Manager asynchrone asyncio.TaskGroup() qui permet d'exécuter de 
manière asynchrone plusieurs taches en meme temps
À noter que le await task1 se fait implicitement avec la méthode __aexit__() du context manager
               await task2

Remarques: 
Tout ce qui est au niveau fonction async def a():...
a() EST UNE COROUTINE NATIVE EN PYTHON SEULEMENT.

 awaitable asyncio.gather(*aws, return_exceptions=False)
    Run awaitable objects in the aws sequence concurrently.
    If any awaitable in aws is a coroutine, 
    it is automatically scheduled as a Task.
    If all awaitables are completed successfully,
     the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in aws.
    If return_exceptions is False (default), 
    the first raised exception is immediately propagated to the task that awaits on gather().
    Other awaitables in the aws sequence won’t be cancelled and will continue to run.
    If return_exceptions is True, 
    exceptions are treated the same as successful results, and aggregated in the result list.
    If gather() is cancelled, 
    all submitted awaitables (that have not completed yet) are also cancelled.
    If any Task or Future from the aws sequence is cancelled,
     it is treated as if it raised CancelledError – the gather() call is not cancelled in this case. 
     This is to prevent the cancellation of one submitted Task/Future to cause other Tasks/Futures to be cancelled.

Execution

À utiliser dans une co-routines seulement:
Mot clé await:
result=await task_or_co_routine:
Attend que la co-routine ou Task Object (co-routine transformé en Task Object)
se termine et retourne le résultat

En groupe:
À utiliser dans une co-routines seulement:
results=await asyncio.gather(*tasks,return_exceptions=True)
-->tasks=Liste de Task Object (meme avec liste de co-routines native peut marcher)
await asyncio.gather(*tasks,return_exceptions=True) permet d'exécuter de manière concourantes
les taches en attendant que toutes les taches se finissent et retourne les résultats des taches (les return des fonctions
/méthodes...) 
sous forme de liste
Rq: si une exeption survient dans la liste des task Object resp co-routines natives ,return_exceptions=True
permet de ne pas stopper l'exécution de tout le monde et retourne pour les taches resp co-routines qui 
ont levées une exception, l'exception comme valeur de retours.

IMPORTANT: Le mot clé await permet d'attendre l'exécution de la/plusieurs task Objects resp co-routines natives et
renvoit tous les résultats, CE MOT CLÉ EST A UTILISÉ UNIQUEMENT DANS DES FONCTIONS/MÉTHODES ASYNCHRONES.



Pour récupérer les résultats d'une méthode/fonction asynchrone depuis un environement non asynchrone:

loop=asyncio.get_event_loop() #running sur une boucle
loop.run_until_complete(f())

-->récupération de la boucle asyncio
-->exécution de la co-routine native f() qui rassemble toutes les executions des co-routines présent dans f().
Python versions 3.10.0–3.10.8 and 3.11.0 this function (and other functions which used it implicitly) emitted a DeprecationWarning if there was no running event loop, 
even if the current loop was set.

UTILISER NOUVELLE VERSION:
result=asyncio.run(f())
--> exécute f() et retourne le résultat: Plus haut niveau que précédement.



Méthode result=await response.read: renvoi string binaire sous forme b"content" ou content est les caractères dans l'encodage de l'url considéré
        encodage des caractères: à noter que str(result) convertit du texte binaire (b'content') en string c'est à dire qui 
        #convertit caractère par caractère présent dans le result (b'<html &amp ....') en unicode sans décodage des caractère.
"""