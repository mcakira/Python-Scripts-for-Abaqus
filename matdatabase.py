#Material data for Titanium
#Consistent Unit System
# Below -x- sign denotes which unit system is chosen
#						-x-	
#mass		kg			mm
#Force		N			N
#Stress		Pa			MPa
#Energy		Joule		mJoule (10^-3 Joule)
#Density	kg/m^3		tonne/mm^3
mdb.models['Model-1'].Material('Titanium')
mdb.models['Model-1'].materials['Titanium'].Density(table=((4.50e-9, ),))
mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200000	,0.3 ),))

#Material data for AISI 1005 grade Steel
mdb.models['Model-1'].Material('AISI1005')
mdb.models['Model-1'].materials['AISI1005'].Density(table=((7.85e-9,),))
mdb.models['Model-1'].materials['AISI1005'].Elastic(table=((200000	,0.29),))

#Material data for Aluminum7076-T61 retrieved from makeitfrom.com
mdb.models['Model-1'].Material('Aluminum7076-T61')
mdb.models['Model-1'].materials['Aluminum7076-T61'].Density(table=((2.69e-9,),))
mdb.models['Model-1'].materials['Aluminum7076-T61'].Elastic(table=((70000	,0.32),))

#Material data for Gold
mdb.models['Model-1'].Material('Gold')
mdb.models['Model-1'].materials['Gold'].Density(table=((19.320E-9,),))
mdb.models['Model-1'].materials['Gold'].Elastic(table=((77.2e3	,0.42 ),))