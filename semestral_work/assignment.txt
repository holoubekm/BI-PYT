KOMENTÁŘE K SEMESTRÁLNÍ PRÁCI
    verze 2015.3

Úkolem vaší semestrální práce je napsat interpretr jazyka brainfuck a to podle následujících požadavků:
~ interpretr bude podporovat rozšíření ! („odděl kód od jeho vstupu“);
~ interpretr bude podporovat rozšíření # („vytiskni ladicí informace“) podle níže popsané specifikace;
~ program bude implementovat obrazovou variantu brainloller, a to jak pro čtení, tak zápis;
~ program bude implementovat obrazovou variantu braincopter, a to jak pro čtení, tak zápis;
~ program bude umět načíst data brainfucku z příkazové řádky, ze standardního vstupu, z textového souboru a z obrázku ve formátu PNG podle níže uvedené specifikace;
~ program bude umět zapsat data brainfucku z obrázku (brainloller i braincopter) do standardního výstupu a do textového souboru podle níže uvedené specifikace;
~ program bude umět zapsat data brainfucku do obrázku ve variantě brainloller podle níže uvedené specifikace.
Součástí odevzdané semestrální práce bude README soubor s popisem vaší implementace.

Specifikace příkazové řádky:
A) Vlastní interpretr:
    brainx.py
    brainx.py bf.b
    brainx.py bl.png
    brainx.py bc.png
~ Varianta bez parametru se bude chovat následovně: Bude-li následována programem v brainfucku uzavřeném v uvozovkách, pokusí se ho vykonat (s výchozím nastavením paměti). Pokud nebude následována programem v brainfucku uzavřeném v uvozovkách, bude se chovat jako interaktivní interpretr -- vyzve uživatele k zadání kódu brainfuckovského programu jako řetězce, který na potvrzení (Enter nebo EOF) zkusí vykonat (jako kdyby ho načetla z externího souboru, to jest celý najednou).
~ Mezi variantou brainloller a braincopter rozlište analýzou obsažených barev. U varianty brainloller je sice napsáno, že jakákoliv jiná mimo základních jedenáct barev je „nop“, ale v praxi (v testech) se můžete celkem spolehnout, že jako „nop“ vystupuje barva jediná (a to černá).
B) Překlad z obrázku (brainloller i braincopter) na výstup nebo do textového souboru:
    brainx.py --lc2f blc.png >bf.b
    brainx.py --lc2f blc.png bf.b
C) Překlad z textového vstupu (soubor se zdrojovým kódem v brainfucku) do PNG-obrázku ve variantě brainloller:
    brainx.py --f2lc -i bf.b -o bl.png
   Překlad z textového vstupu (soubor se zdrojovým kódem v brainfucku) a PNG-obrázku do PNG-obrázku ve variantě braincopter:
    brainx.py --f2lc -i bf.b obr.png -o bc.png
~ Obě varianty tedy odlišuje počet parametrů přepínače „-i“!
D) Testovací a ladicí výpisy v podobě souborů „debug_NN.log“, kde NN jsou postupně čísla 01, 02 atd. podle počtu vyžádaných výstupů, budou aktivovány následujícími přepínači:
    brainx.py -t ..
    brainx.py --test ..
E) Pro potřeby podrobného testování implementace bude program umět rozpoznat a zpracovat následující přepínače:
    brainx.py -m b'...'   |   brainx.py --memory b'...'
        ~ počáteční stav paměti interpretru v podobě pythoního bajtového řetězce
    brainx.py -p N   |   brainx.py --memory-pointer N
        ~ počáteční ukazatel do paměti interpretru v podobě nezáporného celého čísla
    brainx.py --pnm   |   brainx.py --pbm
        ~ zapíše vstupní/výstupní obrázky také ve formě PBM/PNM, a to ve formátu P6, přičemž oddělovačem jednotlivých polí hlavičky a dat bude právě jedna mezera
F) Program bude poskytovat nápovědu na příkazové řádce ve formě standardních přepínačů:
    brainx.py -h
    brainx.py --help
G) Při pokusu o zpracování PNG-vstupu vyhodí v případě chyby následující výjimky:
    PNGWrongHeaderError
        ~ předložený soubor není PNG
        ~ návratová hodnota 4
    PNGNotImplementedError
        ~ předložený soubor je sice PNG, ale používá části standardu, které jsme neimplementovali
        ~ návratová hodnota 8
~ Spolu s výjimkami dá o programu ukončeném chybou vědět i pomocí odpovídající návratové hodnoty (viz sys.exit(N)).

Specifikace ladicích a testovacích informací:
~ Vždy, když interpretr narazí na příkaz #, zapíše do externího souboru „debug_NN.log“ s UNIXovými konci řádek (kde NN jsou postupně čísla 01, 02 atd. podle počtu vyžádaných výstupů) následující informace v uvedeném tvaru:
A) Společné části pro všechny varianty vstupu/výstupu (tedy brainfuck, brainloller a braincopter):
    # program data
    "__vstupní brainfuckovský program bez komentářů (a otáčecích instrukcí) v podobě pythoního řetězce__"
    \n
    # memory
    b"__aktuální stav paměti interpretru v podobě pythoního bajtového řetězce__"
    \n
    # memory pointer
    N __ukazatel aktuální pozice do paměti interpretru jako pythoní int__
    \n
    # output
    b"__aktuální výstup vykonané části brainfuckovského programu v podobě pythoního bajtového řetězce__"
    \n
~ každá část výpisu bude uvozena příslušnou komentářovou hlavičkou;
~ pod každou částí výstupu (hlavička + data) bude jedna prázdná (pythoní) řádka
~ ukázka struktury souboru je v přiloženém ukázkovém archivu.
B) Pro vstup/výstup z/do obrazových dat (tedy varianta brainloller a braincopter) o n sloupcích a m řádcích:
~ pro vstupní obrázek seznam barvových dat obrázku v podobě seznamů řádek obsahujících RGB-trojce, tj.
    # RGB input
    [
        [ (R01, G01, B01), ...,  (R0n, G0n, B0n)],
        ...
        [ (Rm1, Gm1, Bm1), ...,  (Rmn, Gmn, Bmn)],
    ]
    \n
~ pro výstupní obrázek seznam barvových dat obrázku v podobě seznamů řádek obsahujících RGB-trojce, tj.
    # RGB output
    [
        [ (R01, G01, B01), ...,  (R0n, G0n, B0n)],
        ...
        [ (Rm1, Gm1, Bm1), ...,  (Rmn, Gmn, Bmn)],
    ]
    \n
~ Odsazení pro seznamy jednotlivých řádek je tvořeno čtyřmi mezerami. Ostatní odsazení jsou jednomezerová.
~ Označení dat se tedy liší pouze slovy „input/output“ v hlavičce. Dejte si pozor, kdy je který obrázek vstupní a/nebo výstupní a kolik jich v dané formě volání programu je!

Poznámky k implementaci a doplňující požadavky:
A) K interpretru:
~ Testy počítají s tím, že interpretr začíná s jednou jedinou nulovou paměťovou buňkou a paměť se postupně zvětšuje, jak je podle zadání programu potřeba. Vaše vnitřní implementace může být samozřejmě úplně jiná, ale uvedenou strukturu musíte umět vypsat do ladicích souborů.
~ Asi většina dostupných brainfuckovských programů očekává jednobajtové paměťové buňky (tj. místo 256 dostanete 0 a z druhé strany místo -1 dostanete 255) a pásku, která se nerozšiřuje pod nulu (tzn. že chce-li se příkaz < posunout pod nulté paměťové místo, zůstane ukazatel na pozici 0). Takto také interpretr napište. (Ale bude-li na vyžádání umět i opačnou variantu, tím lépe.)
~ Možná pro vstup z klávesnice vymyslíte lepší řešení, než je navržené v přednáškách, ale v tom případě ho důkladně popište v README.
B) K implementaci PNG:
~ Pro čtení a zápis PNG nepoužijete žádné externí knihovny, nýbrž si napíšete vlastní. To se netýká výpočtu CRC a algoritmu komprese -- pro ty použijte příslušné nástroje z interní knihovny.
~ Pro čtení i zápis PNG stačí podpora pouze IHDR-hlavičky 'mn82000', kde 'm' a 'n' jsou šířka a výška obrázku v pixelech. (Tedy žádný alfa-kanál, žádné prokládání a vůbec.) Na vše ostatní vyhazujete „PNGNotImplementedError“. (Ovšem tato výjimka se netýká nepovinných hlaviček!)
~ Obrázky generované či použité pro brainloller a braincopter budou mít tvar obdélníku, jehož každá strana bude mít více než jeden pixel. (Takže žádné psaní instrukcí do jedné řádky zleva doprava :-)
C) K testům:
~ Testy předpokládají jistou základní strukturu aplikace (adresář brainx s hlavním spustitelným souborem __main__.py), ale jinak kladou na vlastní implementaci minimální požadavky. (Tudíž čekám co semestrálka, to originální dílo ;-)
~ Uvedení přepínače „-t“, resp. „--test“, má stejný efekt, jako kdyby ve výkonnové části kódu brainfuckovského programu byl na posledním místě symbol „#“.
~ Bude-li vám nějaký test padat, můžete si pochopitelně odkomentovat příslušný chybový výpis, ale lepší je pustit samostatně váš program s příslušnou příkazovou řádkou.

Základní výukové materiály:
~ Základní přehled jazyka (včetně obou obrazových variant a poznámek k implementaci) je k dispozici na adresách:
    http://vyuka.ookami.cz/materialy/brainfuck/overview.xml
    http://vyuka.ookami.cz/materialy/brainfuck/programming.xml
~ Základní přehled obrazových formátů PNM a PNG je k dispozici na adresách:
    http://vyuka.ookami.cz/materialy/media/pnm.xml
    http://vyuka.ookami.cz/materialy/media/png.xml
