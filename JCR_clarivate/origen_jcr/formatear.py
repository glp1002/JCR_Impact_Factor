# import pandas as pd
# import csv
# archivo = pd.read_csv('./listados_jcr/JCR_2017-All_Journals.csv')


# # Seleccionamos solo la categoría ARTIFICIAL INTELLIGENCE.
# ai_rows = archivo.loc[archivo['Category'] == 'COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE']
# rename_rows = ai_rows.rename(columns={'Full Journal Title': 'Journal name', 
#                                       'JCR Abbreviated Title': 'JCR Abbreviation', 
#                                       'Journal Impact Factor': '2017 JIF',
#                                       'Total Cites': 'Total Citations',
#                                       'Journal Impact Factor': '2017 JIF'
#                                       })



# df = pd.DataFrame(data={'Journal name': rename_rows['Journal name'], 
#                         'JCR Abbreviation': rename_rows['JCR Abbreviation'],
#                         'ISSN': rename_rows['ISSN'],
#                         'eISSN': rename_rows['ISSN'],
#                         'Category': rename_rows['Category'],
#                         'Total Citations' : rename_rows['Total Citations'],
#                         '2017 JIF' : rename_rows['2017 JIF']
#                         })
# df.to_csv("./JCR_AI_2017.csv", sep=',',index=False)





# import pandas as pd
# import csv
# archivo = pd.read_excel('JCR2020.xls', "JCR 2020", header=1)


# # # Seleccionamos solo la categoría ARTIFICIAL INTELLIGENCE.
# # ai_rows = archivo.loc[archivo['Category'] == 'COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE']
# rename_rows = archivo.rename(columns={'Full Journal Title': 'Journal name', 
#                                       #'JCR Abbreviated Title': 'JCR Abbreviation', 
#                                       'Journal Impact Factor': '2020 JIF',
#                                       'Impact Factor without Journal Self Cites' : 'Total Citations'
#                                       #'Total Cites': 'Total Citations'
#                                       })

# rename_rows = rename_rows.replace({"****-****" : "N/A"})
# rename_rows['2020 JIF'] = rename_rows['2020 JIF'].replace({"Not Available" : "N/A"})

# print(rename_rows.head())
# df = pd.DataFrame(data={'Journal name': rename_rows['Journal name'], 
#                         'JCR Abbreviation': rename_rows['Journal name'],
#                         'ISSN': rename_rows['ISSN'],
#                         'eISSN': rename_rows['ISSN'],
#                         'Category': rename_rows['ISSN'],
#                         'Total Citations' : rename_rows['Total Citations'],
#                         '2020 JIF' : rename_rows['2020 JIF']
#                         })
# df.to_csv("./JCR_AI_2020.csv", sep=',',index=False)



# import pandas as pd
# import csv
# archivo = pd.read_excel('latestJCRlist2022.xlsx', header=0)


# # # Seleccionamos solo la categoría ARTIFICIAL INTELLIGENCE.
# # ai_rows = archivo.loc[archivo['Category'] == 'COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE']
# rename_rows = archivo.rename(columns={'journal_name': 'Journal name', 
#                                       'issn' : 'ISSN',
#                                       'eissn' : 'eISSN',
#                                       'category': 'Category', 
#                                       'if_2022': '2022 JIF',
#                                       'citations': 'Total Citations'
#                                       })

# print(rename_rows)
# # rename_rows = rename_rows.loc[archivo['Category'] == 'COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE']

# print(rename_rows.head())
# df = pd.DataFrame(data={'Journal name': rename_rows['Journal name'], 
#                         'JCR Abbreviation': rename_rows['Journal name'],
#                         'ISSN': rename_rows['ISSN'],
#                         'eISSN': rename_rows['eISSN'],
#                         'Category': rename_rows['Category'],
#                         'Total Citations' : rename_rows['Total Citations'],
#                         '2022 JIF' : rename_rows['2022 JIF']
#                         })
# df.to_csv("./JCR_AI_2022.csv", sep=',',index=False)





# import pandas as pd
# import csv
# archivo = pd.read_excel('JCR_completo.ods', "JCR AI 2010", header=0,  engine='odf')


# rename_rows = archivo.rename(columns={#'Full Journal Title': 'Journal name', 
#                                       'Abbreviated Journal Title' :  'JCR Abbreviation', #'JCR Abbreviated Title': 'JCR Abbreviation',
#                                       'Impact Factor': '2010 JIF', #'Journal Impact Factor': '2010 JIF',
#                                       'Total Cites': 'Total Citations'
#                                       })


# rename_rows = rename_rows.replace({"Not Available" : "N/A"})
# salida = []
# salida.extend(['COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE'] * len(rename_rows['2010 JIF']))
# salida2 = []
# salida2.extend(['N/A'] * len(rename_rows['2010 JIF']))


# print(rename_rows.head())
# df = pd.DataFrame(data={'Journal name': salida2, #rename_rows['Journal name'], 
#                         'JCR Abbreviation': rename_rows['JCR Abbreviation'],
#                         'ISSN': rename_rows['ISSN'],
#                         'eISSN': rename_rows['ISSN'],
#                         'Category': salida,
#                         'Total Citations' : rename_rows['Total Citations'],
#                         '2010 JIF' : rename_rows['2010 JIF']
#                         })
# df.to_csv("./JCR_AI_2010.csv", sep=',',index=False)


# import pandas as pd
# import csv
# archivo = pd.read_excel('JCR_completo.ods', "JCR Computer Science 2004", header=4,  engine='odf')


# rename_rows = archivo.rename(columns={#'Full Journal Title': 'Journal name', 
#                                       'Abbreviated Journal Title' :  'JCR Abbreviation', #'JCR Abbreviated Title': 'JCR Abbreviation',
#                                       'ImpactFactor': '2004 JIF', #'Journal Impact Factor': '2010 JIF',
#                                       "2004 TotalCites": 'Total Citations'
#                                       })

# rename_rows = rename_rows.replace({"Not Available" : "N/A"})
# salida = []
# salida.extend(['COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE'] * len(rename_rows['2004 JIF']))
# salida2 = []
# salida2.extend(['N/A'] * len(rename_rows['2004 JIF']))


# print(rename_rows.head())
# df = pd.DataFrame(data={'Journal name': salida2, #rename_rows['Journal name'], 
#                         'JCR Abbreviation': rename_rows['JCR Abbreviation'],
#                         'ISSN': rename_rows['ISSN'],
#                         'eISSN': rename_rows['ISSN'],
#                         'Category': salida,
#                         'Total Citations' : rename_rows['Total Citations'],
#                         '2004 JIF' : rename_rows['2004 JIF']
#                         })
# df.to_csv("./JCR_AI_2004.csv", sep=',',index=False)
