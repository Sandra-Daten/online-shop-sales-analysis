
import pandas as pd

print ("\n================================ 1. UCITAVANJE I UPOZNAVANJE PODATAKA ===================================\n");

# -----------------------------------------------------------------------------------------
# Ucitavanje podataka
# -----------------------------------------------------------------------------------------

df_customers = pd.read_csv("data/customers.csv");
df_products = pd.read_csv("data/products.csv");
df_orders = pd.read_csv("data/orders.csv");
df_order_items = pd.read_csv('data/order_items.csv');

# -----------------------------------------------------------------------------------------
# Upoznavanje podataka
# -----------------------------------------------------------------------------------------

def upoznavanje_podataka(naslov, tabela):

    print(f"// TABLE {naslov}");

    rows, columns = tabela.shape

    print(f"rows: {rows}, columns: {columns}");
    print(tabela.columns.tolist());
    print(tabela.dtypes);
    print(tabela.head());

upoznavanje_podataka("CUSTOMERS", df_customers);
upoznavanje_podataka("PRODUCTS",df_products);
upoznavanje_podataka("ORDERS",df_orders);
upoznavanje_podataka("ORDER_ITEMS",df_order_items);



print ("\n================================ 2. PROVERA KVALITETA PODATAKA ================================");

# -----------------------------------------------------------------------------------------
# Missing value
# -----------------------------------------------------------------------------------------

def missing_values(naziv, tabela):
    print(f"\nMissing values - {naziv}");
    print(tabela.isna().sum());


missing_values("CUSTOMERS", df_customers);
missing_values("PRODUCTS", df_products);
missing_values("ORDERS", df_orders);
missing_values("ORDER_ITEMS", df_order_items);

# Zapis ima nedostajuću vrednost za country, a ostale vrednosti (Test User, test@email.com) ukazuju na testni zapis.
# Zbog toga cemo ga uklaniti iz skupa podataka umesto da pokušavamo da dopunimo nedostajuću državu.
# Pre ovoga treba proveriti da li se customer_id = 18 nalazi u tabeli orders

print(df_customers[df_customers["country"].isna()]);
print(df_orders[df_orders["customer_id"] == 18]);

# Customer 18 nema porudzbine, pa se zapis uklanja iz customers tabele.

# -----------------------------------------------------------------------------------------
# Duplicates
# -----------------------------------------------------------------------------------------

def duplikati(naziv, tabela):
    print(f"\nDuplikati - {naziv}");
    print(tabela.duplicated().sum());

duplikati("CUSTOMERS", df_customers);
duplikati("PRODUCTS", df_products);
duplikati("ORDERS", df_orders);
duplikati("ORDER_ITEMS", df_order_items);

print(df_orders[df_orders.duplicated()]);

# Pronadjen je jedan duplikat u orders tabeli (order_id = 15034).
# Duplikat ce biti uklonjen tokom ciscenja.

# -----------------------------------------------------------------------------------------
# Pogresni tipovi podataka
# -----------------------------------------------------------------------------------------
# registration_date i order_date su ucitani kao string vrednosti.
# Obe kolone ce tokom ciscenja biti konvertovane u datetime.

# -----------------------------------------------------------------------------------------
# Negativne quantity vrednosti
# -----------------------------------------------------------------------------------------

print(df_order_items[df_order_items["quantity"] < 0]);

print(df_orders[df_orders["order_id"] == 15012]);
print(df_products[df_products["product_id"] == 101]);

# order_item_id = 67 ima quantity = -3.
# Nije moguce pouzdano utvrditi da li je ispravna vrednost (+)3, pa se zapis uklanja umesto proizvoljnog ispravljanja vrednosti.

# -----------------------------------------------------------------------------------------
#  Cene manje ili jednake nuli
# -----------------------------------------------------------------------------------------

print(df_products[df_products["price"] <= 0]);
print(df_order_items[df_order_items["product_id"] == 121]);

# product_id = 121 ima price = 0 i naziv "Broken Product".
# Proizvod i povezani order_item_id = 68 bice uklonjeni.

# -----------------------------------------------------------------------------------------
#  Da li je negde cost > price?
# -----------------------------------------------------------------------------------------

print(df_products[df_products["cost"] > df_products["price"]]);
print(df_order_items[df_order_items["product_id"] == 122]);

# product_id = 122 ima cost veci od price.
# Ispravnu vrednost nije moguce pouzdano utvrditi, pa se proizvod i povezani order_item_id = 69 uklanjaju.
# Porudzbina 15020 ostaje jer sadrzi druge validne stavke.

# -----------------------------------------------------------------------------------------
# Nepostojee customer ID-jeve
# -----------------------------------------------------------------------------------------

print(
    df_orders[
        ~df_orders["customer_id"].isin(df_customers["customer_id"])
    ]
);

print(df_order_items[df_order_items["order_id"] == 15032]);

# order_id = 15032 pripada customer_id = 8888 koji ne postoji u customers tabeli.
# Porudzbina 15032 i povezani order_item_id = 62 bice uklonjeni.

# -----------------------------------------------------------------------------------------
# Nepostojeci product ID-jeve
# -----------------------------------------------------------------------------------------

print(
    df_order_items[
        ~df_order_items["product_id"].isin(df_products["product_id"])
    ]
);

print(df_order_items[df_order_items["order_id"] == 15010]);

# order_item_id = 66 sadrzi product_id = 999 koji ne postoji u products tabeli.
# Stavka 66 bice uklonjena, dok order_id = 15010 ostaje jer sadrzi druge validne proizvode.

# -----------------------------------------------------------------------------------------
# Neispravni datumi
# -----------------------------------------------------------------------------------------

print("\n// Neispravni datumi u tabeli 'df_customers':\n\n",
    df_customers[
        pd.to_datetime(
            df_customers["registration_date"],
            errors="coerce"
        ).isna()
    ]
);

print("\n// Neispravni datum u tabeli 'df_orders':\n\n",
    df_orders[
        pd.to_datetime(
            df_orders["order_date"],
            errors="coerce"
        ).isna()
    ]
);

# Pronadjene su neispravne vrednosti "invalid_date" u registration_date i "not_a_date" u order_date.
# Zapisi ostaju u datasetu, a neispravni datumi ce tokom ciscenja biti konvertovani u NaT.



print ("\n================================ 3. CISCENJE ================================\n");

df_customers_clean = df_customers.copy();
df_products_clean = df_products.copy();
df_orders_clean = df_orders.copy();
df_order_items_clean = df_order_items.copy();

# -----------------------------------------------------------------------------------------
# Uklanjanje testnog customer-a sa nedostajucom country vrednoscu
# -----------------------------------------------------------------------------------------

df_customers_clean = df_customers_clean[df_customers_clean["customer_id"] != 18];

# -----------------------------------------------------------------------------------------
# Uklanjanje proizvoda sa nevalidnim price/cost vrednostima
# -----------------------------------------------------------------------------------------

df_products_clean = df_products_clean[df_products_clean["product_id"] != 121];
df_products_clean = df_products_clean[df_products_clean["product_id"] != 122];

# -----------------------------------------------------------------------------------------
# Uklanjanje duplikata
# -----------------------------------------------------------------------------------------

df_orders_clean = df_orders_clean.drop_duplicates();

# -----------------------------------------------------------------------------------------
# Uklanjanje porudzbine koja pripada nepostojecem customer-u
# -----------------------------------------------------------------------------------------

df_orders_clean = df_orders_clean[df_orders_clean["order_id"] != 15032];

# -----------------------------------------------------------------------------------------
# Uklanjanje nevalidnih stavki porudzbina
# -----------------------------------------------------------------------------------------

invalid_order_items = [62, 66, 67, 68, 69];

df_order_items_clean = df_order_items_clean[
    ~df_order_items_clean["order_item_id"].isin(invalid_order_items)
];

# -----------------------------------------------------------------------------------------
# Konverzija datuma
# -----------------------------------------------------------------------------------------

df_customers_clean["registration_date"] = pd.to_datetime(
    df_customers_clean["registration_date"],
    errors="coerce"
);

df_orders_clean["order_date"] = pd.to_datetime(
    df_orders_clean["order_date"],
    errors="coerce"
);

# -----------------------------------------------------------------------------------------
# Standardizacija country vrednosti
# -----------------------------------------------------------------------------------------

df_customers_clean["country"] = df_customers_clean["country"].str.capitalize();

# -----------------------------------------------------------------------------------------
# Provera ociscenih podataka
# -----------------------------------------------------------------------------------------

print(df_customers_clean.dtypes);
print(df_orders_clean.dtypes);
print(df_customers_clean["country"].value_counts());

# -----------------------------------------------------------------------------------------
# Cuvanje ociscenih podataka
# -----------------------------------------------------------------------------------------

df_customers_clean.to_csv("output/customers_clean.csv", index=False);
df_products_clean.to_csv("output/products_clean.csv", index=False);
df_orders_clean.to_csv("output/orders_clean.csv", index=False);
df_order_items_clean.to_csv("output/order_items_clean.csv", index=False);



print ("\n================================ 4. SPAJANJE PODATAKA ================================\n");

df_customers_orders = pd.merge(
    df_customers_clean,
    df_orders_clean,
    on="customer_id",
    how="inner"
);

df_products_items = pd.merge(
    df_products_clean,
    df_order_items_clean,
    on="product_id",
    how="inner"
);

df_joined = pd.merge(
    df_customers_orders,
    df_products_items,
    on="order_id",
    how="inner"
);

# -----------------------------------------------------------------------------------------
# Provera spojenog DataFrame-a
# -----------------------------------------------------------------------------------------

print(df_joined.shape);
print(df_joined.columns.tolist());
print("Broj duplikata:", df_joined.duplicated().sum());
print("Missing values:");
print(df_joined.isna().sum());

# Jedini ocekivani missing podatak je NaT za prethodno detektovan neispravan order_date.
print(df_joined[df_joined.isna().any(axis=1)]);



print ("\n================================ 5. REVENUE I PROFIT ================================\n");

# -----------------------------------------------------------------------------------------
# Metrike: revenue, total_cost, profit, profit_margin
# -----------------------------------------------------------------------------------------

df_joined["revenue"] = (
    df_joined["price"] * df_joined["quantity"]
) * (1 - df_joined["discount"]);

df_joined["total_cost"] = df_joined["cost"] * df_joined["quantity"];
df_joined["profit"] = df_joined["revenue"] - df_joined["total_cost"];
df_joined["profit_margin"] = df_joined["profit"] / df_joined["revenue"];

# redosled kolona u finalnom dataset-u

# print(df_joined.columns)

df_joined = df_joined[
    [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country",
        "registration_date",
        "order_id",
        "order_date",
        "order_item_id",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "price",
        "cost",
        "discount",
        "revenue",
        "total_cost",
        "profit",
        "profit_margin"

    ]
];

# -----------------------------------------------------------------------------------------
# Ukupne metrike
# -----------------------------------------------------------------------------------------

final_revenue = df_joined["revenue"].sum();
final_cost = df_joined["total_cost"].sum();
final_profit = df_joined["profit"].sum();
final_profit_margin = final_profit / final_revenue;
average_order_value = final_revenue / df_joined["order_id"].nunique();

print(f"Ukupni revenue: {final_revenue:.2f}");
print(f"Ukupni cost: {final_cost:.2f}");
print(f"Ukupni profit: {final_profit:.2f}");
print(f"Ukupna profitna margina: {final_profit_margin * 100:.2f}%");
print(f"Prosecna vrednost porudzbine: {average_order_value:.2f}");

# -----------------------------------------------------------------------------------------
# Cuvanje finalnog dataseta spremnog za analizu
# -----------------------------------------------------------------------------------------

df_joined.to_csv("output/sales_clean.csv", index=False);



print ("\n================================ 6. ANALIZA PRODAJE ================================\n");

# Osnovna analiza
# -----------------------------------------------------------------------------------------

total_orders = df_joined["order_id"].nunique();
unique_customers = df_joined["customer_id"].nunique();
total_sold_products = df_joined["quantity"].sum();

print(f"Ukupan broj porudzbina: {total_orders}");
print(f"Broj jedinstvenih kupaca: {unique_customers}");
print(f"Ukupan broj prodatih proizvoda: {total_sold_products}");
print(f"Ukupan revenue: {final_revenue:.2f}");
print(f"Ukupan profit: {final_profit:.2f}");

# Analiza proizvoda
# -----------------------------------------------------------------------------------------

# Najprodavaniji proizvod po kolicini

quantity_by_product = df_joined.groupby("product_name")["quantity"].sum();

top_quantity_product = quantity_by_product.idxmax();
highest_product_quantity = quantity_by_product.max();

print(
    f"Najprodavaniji proizvod je {top_quantity_product} "
    f"sa {highest_product_quantity} prodatih jedinica."
);

# Proizvod sa najvecim revenue

revenue_by_product = df_joined.groupby("product_name")["revenue"].sum();

top_revenue_product = revenue_by_product.idxmax();
highest_product_revenue = revenue_by_product.max();

print(
    f"Proizvod sa najvecim revenue je {top_revenue_product} "
    f"sa revenue od {highest_product_revenue:.2f}."
);

# Proizvod sa najvecim profitom

profit_by_product = df_joined.groupby("product_name")["profit"].sum();

top_profit_product = profit_by_product.idxmax();
highest_product_profit = profit_by_product.max();

print(
    f"Proizvod sa najvecim profitom je {top_profit_product} "
    f"sa profitom od {highest_product_profit:.2f}."
);

# Proizvod sa najvecom profitnom marginom

profit_margin_by_product = profit_by_product / revenue_by_product;
top_margin_product = profit_margin_by_product.idxmax();
highest_product_margin = profit_margin_by_product.max();

print(
    f"Proizvod sa najvecom profitnom marginom je "
    f"{top_margin_product} sa marginom od "
    f"{highest_product_margin * 100:.2f}%."
);

# Analiza kategorija
# -----------------------------------------------------------------------------------------

revenue_by_category = df_joined.groupby("category")["revenue"].sum();
profit_by_category = df_joined.groupby("category")["profit"].sum();
profit_margin_by_category = profit_by_category / revenue_by_category;

# Kategorija sa najvecim revenue

top_revenue_category = revenue_by_category.idxmax();
highest_category_revenue = revenue_by_category.max();

print(
    f"Kategorija sa najvecim revenue je {top_revenue_category} "
    f"sa revenue od {highest_category_revenue:.2f}."
);

# Kategorija sa najvecim profitom

top_profit_category = profit_by_category.idxmax();
highest_category_profit = profit_by_category.max();

print(
    f"Kategorija sa najvecim profitom je {top_profit_category} "
    f"sa profitom od {highest_category_profit:.2f}."
);

# Kategorija sa najvecom profitnom marginom

top_margin_category = profit_margin_by_category.idxmax();
highest_category_margin = profit_margin_by_category.max();

print(
    f"Kategorija sa najvecom profitnom marginom je "
    f"{top_margin_category} sa marginom od "
    f"{highest_category_margin * 100:.2f}%."
);



print ("\n================================ 7. CUSTOMER ANALYSIS ================================\n");

# -----------------------------------------------------------------------------------------
# Top 10 kupaca po potrosnji
# -----------------------------------------------------------------------------------------

df_joined["Customer"] = df_joined["first_name"] + " " + df_joined["last_name"];

customers_analysis = df_joined.groupby(
    ["customer_id", "Customer"]
).agg(
    Orders=("order_id", "nunique"),
    Revenue=("revenue", "sum"),
    Profit=("profit", "sum")
);

top10_customers = customers_analysis.nlargest(10, "Revenue");

print(top10_customers);

# -----------------------------------------------------------------------------------------
# Kupac sa najvise porudzbina
# -----------------------------------------------------------------------------------------

top_orders_customer = top10_customers["Orders"].idxmax();
highest_customer_orders = top10_customers["Orders"].max();

print(
    f"{top_orders_customer[1]} ima najvise porudzbina - "
    f"{highest_customer_orders} porudzbina."
);

# -----------------------------------------------------------------------------------------
# Kupac sa najvecom potrosnjom
# -----------------------------------------------------------------------------------------

top_revenue_customer = top10_customers["Revenue"].idxmax();
highest_customer_revenue = top10_customers["Revenue"].max();

print(
    f"{top_revenue_customer[1]} je najvise potrosio - "
    f"{highest_customer_revenue:.2f}."
);

# -----------------------------------------------------------------------------------------
# Kupac koji donosi najveci profit
# -----------------------------------------------------------------------------------------

top_profit_customer = top10_customers["Profit"].idxmax();
highest_customer_profit = top10_customers["Profit"].max();

print(
    f"{top_profit_customer[1]} donosi najveci profit "
    f"u iznosu od {highest_customer_profit:.2f}."
);







