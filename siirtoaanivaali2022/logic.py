import opavote
from vaali import Vaali
from datetime import datetime
import locale

print("Hello world")

# luo vaali

vaali = Vaali()

# lue tiedosto ja luo lipukkeet. anna ehdokas- ja lipukelistat opavoten käyttöön
tiedosto = "testivaali.txt"

opavote.luo_lipukkeet(tiedosto, vaali)
# vaali.alusta_aanikynnys()
# print(f"äänikynnys: {vaali.hae_aanikynnys()}")

# luo tiedostot laskennan ja tulosten tallentamiseen

loc = locale.setlocale(locale.LC_ALL, 'fi_FI.UTF-8')

aika = datetime.now()
tulokset = f"vaalit/{vaali.hae_vaalin_nimi().replace(' ', '_')}_{aika.strftime('%Y%m%d%_H%M%S')}_tulokset.txt"
laskenta = f"vaalit/{vaali.hae_vaalin_nimi().replace(' ', '_')}_{aika.strftime('%Y%m%d%_H%M%S')}_laskenta.txt"

mjono = vaali.hae_vaalin_nimi() + "\n"
mjono += aika.strftime("%x %X") + "\n"
mjono += f"Ehdokkaita: {vaali.hae_ehdokkaat().hae_ehdokkaiden_lkm()}\tValitaan: {vaali.hae_valittavien_lkm()}\n\n"
mjono += str(vaali.hae_ehdokkaat()) + "\n\n"

with open(tulokset, "w") as tiedosto:
    tiedosto.write(mjono)

with open(laskenta, "w") as tiedosto:
    tiedosto.write(mjono)


# laskentakierros, toista kunnes valittuja tarpeeksi

kierros = 1

while kierros < 11:

    valitut_kierroksen_alussa = vaali.hae_valittujen_lkm()

    with open(laskenta, "a") as tiedosto:
        mjono = f"Kierros {kierros}"
        tiedosto.write(f"\n{mjono}\n")
        tiedosto.write("=" * len(mjono) + "\n\n")
        tiedosto.write(f"Valittujen lkm kierroksen alussa: {valitut_kierroksen_alussa}\n")

    #   1. Ehdokas:Ehdokkaat laske äänet

    # jaa ääni lipukkeella ehdokkaille ennen äänien hakemista

    vaali.jaa_aanet_lipukkeilla()

    vaali.laske_aanet()

    with open(laskenta, "a") as tiedosto:
        tiedosto.write(str(vaali.hae_ehdokkaat()) + "\n\n")

    #   2. Lipukkeet äänihukka

    vaali.paivita_aanihukka()

    with open(laskenta, "a") as tiedosto:
        tiedosto.write(f"äänihukka: {vaali.hae_aanihukka()}\n")

    #   3. Äänikynnys update

    vaali.paivita_aanikynnys()
    
    with open(laskenta, "a") as tiedosto:
        tiedosto.write(f"äänikynnys: {vaali.hae_aanikynnys()}\n\n")

#   Ehdokkaat valitse äänikynnyksen ylittäneet tai pudota vähiten ääniä saanut
#       jos tasapeli, toista laskentakierrosta poikkeavilla säännöillä (tee laskentakierroksesta oma funktio ja kutsu sitä rekursiivisesti)

    vaali.valitse_ehdokkaat()

    with open(laskenta, "a") as tiedosto:
        tiedosto.write(str(vaali.hae_ehdokkaat()) + "\n\n")

    #   4. Ehdokas:Ehdokkaat ehdokas.updateP

    vaali.paivita_p_arvot()

    with open(laskenta, "a") as tiedosto:
        tiedosto.write("Päivitetään p-arvot\n\n")
        tiedosto.write(str(vaali.hae_ehdokkaat()) + "\n\n")

    with open(laskenta, "a") as tiedosto:
        tiedosto.write(f"Valittujen lkm: {vaali.hae_valittujen_lkm()}\n\n")

    #print(str(valitut_kierroksen_alussa))

    if valitut_kierroksen_alussa - vaali.hae_valittujen_lkm() == 0:
        vaali.pudota_ehdokas()
        with open(laskenta, "a") as tiedosto:
            tiedosto.write("Pudotetaan ehdokas\n\n")
            #tiedosto.write(str(vaali.hae_ehdokkaat()) + "\n")

    with open(laskenta, "a") as tiedosto:
        tiedosto.write("Ehdokkaat kierroksen lopussa\n\n")
        tiedosto.write(str(vaali.hae_ehdokkaat()) + "\n\n")

    kierros += 1





