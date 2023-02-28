from habanero import Crossref
cr = Crossref()
result = cr.works(query = "Exploring the Dynamics of Quantum Entanglement in Multi-Particle Systems")
print(result['message']['items'][0]['DOI']) # Salida: 10.1007/3-540-49208-9_1