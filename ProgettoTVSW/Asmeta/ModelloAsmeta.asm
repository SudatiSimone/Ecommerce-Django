asm ModelloAsmeta

import StandardLibrary
import CTLlibrary
import LTLlibrary

signature: 
 
	abstract domain Utente
	domain Prodotto subsetof String
	domain SubInteger subsetof Integer
	
	enum domain State = {START | INSERIREID | CHECKID | INSERIREPWD | CHECKPWD | CHOOSESERVICE |  CARRELLO | ADD_PRODUCT }
	enum domain Service = {CART | CHANGEPWS | ADD_PRODUCT_OR_EXIT | EXIT}
	enum domain Decision = {PAY | CONTINUE }
	
	dynamic controlled currentState : State
	dynamic controlled total: SubInteger
	dynamic controlled messaggio : String
	dynamic controlled currentUserID : Utente
	dynamic controlled currentPwd : String
	dynamic controlled prodotto : Prodotto
	dynamic controlled currentRFT : Integer
	dynamic controlled listaProdotti : Utente -> Seq(Prodotto)
	dynamic controlled numProducts: SubInteger
	
	dynamic monitored id_utente : Utente
	dynamic monitored prod : String
	dynamic monitored password : String
	dynamic monitored selectedService: Service
	dynamic monitored decision : Decision
	dynamic monitored insertQuantity: SubInteger
	dynamic monitored insertPrice: SubInteger
	
	
	derived utentePassword: Utente -> String
	
	static isValidID: Utente -> Boolean
	static isValidPwd: String -> Boolean
	static utente1 : Utente
	static utente2 : Utente


definitions:

	domain Prodotto = {"scarpe", "maglia", "pantaloni","sciarpa"}
	domain SubInteger = {0..10}
	
	function isValidID($id in Utente) =
		if(exist $u in Utente with $id = $u) 
		then
			true
		else
			false
		endif
		
	
		
	function utentePassword ($ut in Utente) =
		if ($ut=utente1)
		then 
			"miao1"
		else
			if ($ut=utente2) 
				then "miao2" 
			endif
		endif
	
	function isValidPwd($pwd in String) =
		if (utentePassword(currentUserID)= $pwd) then 
			true
		else
			false
		endif
	
	macro rule r_AddProduct =
		if (currentState = ADD_PRODUCT) then
		par
			total := total + insertPrice*insertQuantity
			numProducts := numProducts + 1
			currentState := CHOOSESERVICE
		endpar
		endif
	
	macro rule r_insertID =
		if(currentState = INSERIREID) then
			par
				currentUserID := id_utente
				currentState := CHECKID
			endpar
		endif

	macro rule r_checkID =
		if(currentState = CHECKID) then
				if(isValidID(currentUserID)) then
					par
						currentState := INSERIREPWD
						messaggio := "Inserire la Password"
					endpar
				else
					par
						currentState := START
						messaggio := "ID Utente inesistente!"
					endpar
				endif
		endif

	macro rule r_insertPWD =
		if(currentState = INSERIREPWD) then
			par
				currentPwd := password
				currentState := CHECKPWD
			endpar
		endif

	macro rule r_checkPWD =
		if(currentState = CHECKPWD) then
			if(isValidPwd(currentPwd)) then
				par
					currentState := CHOOSESERVICE
					messaggio := "Di che servizio vuoi usufruire? CARRELLO o SOMMARIO o CHANGEPWS o EXIT"
				endpar
			else
				par
					currentState := START
					messaggio := "Password errata!"
				endpar
			endif
		endif


	macro rule r_chooseService =
		if(currentState=CHOOSESERVICE) then
			par
				if(selectedService=ADD_PRODUCT_OR_EXIT) then
					par
						currentState := ADD_PRODUCT
						messaggio := "Questo è il sommario dell'attuale ordine(prodotto selezionato)"
					endpar
				endif
				
				if(selectedService=CART) then
					par
						currentState := CARRELLO
						messaggio := "Quale prodotto vuoi aggiungere al carrello? scarpe, sciarpa, pantaloni o maglia"
						prodotto := prod
					endpar
				endif
				
				if(selectedService=CHANGEPWS) then
					par
						//TODO: per implementazioni future!
						currentState:= START
						messaggio := "Uscita dal sistema!"
					endpar
				endif
				
				if(selectedService=EXIT) then
					par
						currentState := START
						messaggio := "Uscita dal sistema!"
					endpar
				endif
				
			endpar
		endif
	

		
	macro rule r_gestioneCarrello =
	if( currentState = CARRELLO ) then
		if( exist unique $t in Prodotto with $t = prodotto ) then
			par
				listaProdotti( currentUserID ) := append( listaProdotti( currentUserID ), prodotto)
				messaggio := concat ("prodotto aggiunto: ", toString( prodotto ) )
				currentState := CHOOSESERVICE
			endpar
		endif
	endif
		
	


	main rule r_Main =
		if(currentState = START) then
			par
				currentState := INSERIREID
				messaggio := "Inserire ID Utente"
			endpar
		else
			par
				r_insertID[]
				r_checkID[]
				r_insertPWD[]
				r_checkPWD[]
				r_chooseService[]
				r_AddProduct[]
				r_gestioneCarrello[]
			endpar
		endif


default init s0:
	function currentState = START
	function listaProdotti( $u in Utente ) = []
	function numProducts = 0 
	function total = 0
