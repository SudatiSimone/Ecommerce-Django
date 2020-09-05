asm ModelloAsmetaSemplificato

import StandardLibrary
import CTLlibrary
import LTLlibrary

signature: 
 
	
	domain SubInteger subsetof Integer
	domain SubInteger2 subsetof Integer
	
	enum domain State = {START | ENTER | CHOOSESERVICE | DECISION | ADD_PRODUCT | OUT }
	enum domain Service = { CHANGEPWS | ADD_PRODUCT_OR_EXIT | EXIT}
	enum domain Decision = {PROCEDE | EXIT2 }
	enum domain Enter ={GO | EXIT1}
	
	dynamic controlled currentState : State
	dynamic controlled total: SubInteger
	dynamic controlled numProducts: SubInteger2
	
	dynamic monitored selectedService: Service
	dynamic monitored decision2 : Decision
	dynamic monitored decision1 : Enter
	dynamic monitored insertQuantity: SubInteger
	dynamic monitored insertPrice: SubInteger
	
	derived correct: Boolean


definitions:

	domain SubInteger = {0..10}
	domain SubInteger2 = {0, 1, 2, 3}
	function correct = numProducts < 3
	
		
	macro rule r_AddProduct =
		if (currentState = ADD_PRODUCT) then
		par
			total := total + insertPrice*insertQuantity
			numProducts := numProducts + 1
			currentState := DECISION
		endpar
		else skip
		endif
		

	macro rule r_chooseService =
		if(currentState=CHOOSESERVICE) then
			par
				if(selectedService=ADD_PRODUCT_OR_EXIT) then
						currentState := ADD_PRODUCT
				endif
				
				if(selectedService=CHANGEPWS) then
						//TODO: per implementazioni future!
						currentState:= START
				endif
				if(selectedService=EXIT) then
						currentState := START
				endif
				
				
			endpar
		else skip
		endif
		
		
	macro rule r_enter =
		if(currentState=ENTER) then
			par
				if(decision1=GO) then
						currentState := CHOOSESERVICE
				endif
				if(decision1=EXIT1) then
						currentState := OUT
				endif
				
				
			endpar
		else skip
		endif
	
		
	macro rule r_decision =
		if(currentState=DECISION) then
			par
				if(decision2=PROCEDE) then
						currentState := CHOOSESERVICE
				endif
				if(decision2=EXIT2) then
						currentState:= OUT
				endif
				
			endpar
		else skip
		endif
		
		
	macro rule r_Stop = 
		currentState := OUT
	
	//CTL
	CTLSPEC ag(numProducts <= 3)
	
	CTLSPEC ag(total <= 300)
	
	CTLSPEC ag(currentState = OUT implies ag(currentState = OUT))
	
	CTLSPEC ef(currentState=OUT)
	
	CTLSPEC ef(currentState=START and numProducts=0 and total=0)
	
	CTLSPEC ag((currentState = ADD_PRODUCT and numProducts=3) implies af(currentState = OUT))

	CTLSPEC ag((currentState = DECISION and decision2 = EXIT2) implies ax(currentState = OUT))
	
	CTLSPEC ag((currentState=ADD_PRODUCT ) implies ax(currentState = CHOOSESERVICE))
	

	main rule r_Main =
		if(currentState = START and correct=true) then
				currentState := ENTER
		else
			if (correct=true)then  
			par
				r_enter[]
				r_chooseService[]
				r_AddProduct[]
				r_decision[]
			endpar
			else
				r_Stop[]
		endif
		endif


default init s0:
	function currentState = START
	function numProducts = 0 
	function total = 0
