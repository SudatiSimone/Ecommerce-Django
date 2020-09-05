from math import sqrt
import icontract


@icontract.require(lambda y_ShippingPosition: y_ShippingPosition > 0,
                   " deve essere positiva la coordinata y di spedizione")
@icontract.require(lambda x_ShippingPosition: x_ShippingPosition > 0,
                   " deve essere positiva la coordinata x di spedizione")
@icontract.require(lambda x_shop: 0 < x_shop < 50,
                   " indirizzo coordinata x del negozio ")
@icontract.require(lambda y_shop: 0 < y_shop < 50,
                   " deve essere positiva la coordinata x di spedizione")
@icontract.ensure(lambda result: 0 < result <= 10,
                  "il costo dev'essere >0 e al massimo=10 ")
def CalculateShipping(x_ShippingPosition: int, y_ShippingPosition: int,
                      x_shop: int, y_shop: int):
    # posizione del magazzino
    x_magazzino = 5
    y_magazzino = 23

    # calcolo della distance
    distance1 = sqrt(
        pow((x_shop - x_magazzino), 2) + pow((y_shop - y_magazzino), 2))
    distance2 = sqrt(pow((x_magazzino - x_ShippingPosition), 2) + pow(
        (y_magazzino - y_ShippingPosition), 2))
    distance = distance1 + distance2

    # calcola la distanza totale tra magazzino e l'indirizzo di spedizione
    costo_al_metro = 0.2
    full_cost = costo_al_metro * distance

    assert full_cost > 0
    if full_cost > 10:
        full_cost = 10
    elif full_cost < 1:
        full_cost = 0

    return full_cost


@icontract.invariant(lambda self: len(str(self.codice)) == 5)
@icontract.invariant(lambda self: self.codice > 0)
class Prodotto:
    def __init__(self, nome, codice, prezzo):
        self.nome = nome
        self.codice = codice
        self.prezzo = prezzo

    def recap(self):
        return f"Prodotto\n Nome:{self.nome}\n Codice:{self.codice}\n Prezzo:{self.prezzo}"


def main():
    costo1 = CalculateShipping(2, 10, 25, 37)
    print("Il costo della spedizione è: " + str(costo1))

    # Viola pre-condizione perchè y shop è >50
    # costo2 = CalculateShipping(2, 10, 25, 51)

    prodotto1 = Prodotto("shampoo", 12345, 10)
    print(prodotto1.recap())

    # Viola l'invariante perchè fatto da 6 cifre
    # prodotto2 = Prodotto("shampo", 123456, 25)

if __name__ == "__main__":
    main()

