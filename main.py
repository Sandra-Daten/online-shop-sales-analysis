
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).parent
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)


def load_data():
    df_customers = pd.read_csv(BASE / "data" / "customers.csv")
    df_products = pd.read_csv(BASE / "data" / "products.csv")
    df_orders = pd.read_csv(BASE / "data" / "orders.csv")
    df_order_items = pd.read_csv(BASE / "data" / "order_items.csv")

    return df_customers, df_products, df_orders, df_order_items


def missing_values(naziv, tabela):
    print(f"\nMissing values - {naziv}")
    print(tabela.isna().sum())


def duplikati(naziv, tabela):
    print(f"\nDuplikati - {naziv}")
    print(tabela.duplicated().sum())


def check_data_quality(df_customers, df_products, df_orders, df_order_items):
    print("\n================================ 2. PROVERA KVALITETA PODATAKA ================================")

    # ------------------------------------------------------------------------------------------------------------------

    # Missing values

    missing_values("CUSTOMERS", df_customers)
    missing_values("PRODUCTS", df_products)
    missing_values("ORDERS", df_orders)
    missing_values("ORDER_ITEMS", df_order_items)

    # Zapis ima nedostajucu vrednost za country, a ostale vrednosti
    # (Test User, test@email.com) ukazuju na testni zapis.
    # Pre uklanjanja proveravamo da li customer_id = 18 ima porudzbine.

    print(df_customers[df_customers["country"].isna()])
    print(df_orders[df_orders["customer_id"] == 18])

    # Customer 18 nema porudzbine, pa se uklanja tokom ciscenja.

    # ------------------------------------------------------------------------------------------------------------------

    # Duplicates

    duplikati("CUSTOMERS", df_customers)
    duplikati("PRODUCTS", df_products)
    duplikati("ORDERS", df_orders)
    duplikati("ORDER_ITEMS", df_order_items)

    print(df_orders[df_orders.duplicated()])

    print("\n// Duplirani kupci prema email adresi:\n")

    duplicate_customers = df_customers[
        df_customers.duplicated(
            subset=["email"],
            keep=False
        )
    ]

    print(duplicate_customers)

    print("\n// Potencijalno duplirane stavke prema order_id i product_id:\n")

    duplicate_order_items = df_order_items[
        df_order_items.duplicated(
            subset=["order_id", "product_id"],
            keep=False
        )
    ]

    print(duplicate_order_items)

    # Pronadjen je duplikat u orders tabeli (order_id = 15034).
    # Duplikat ce biti uklonjen tokom ciscenja.

    # ------------------------------------------------------------------------------------------------------------------

    # Pogresni tipovi podataka


    # registration_date i order_date su ucitani kao string vrednosti.
    # Tokom ciscenja bice konvertovani u datetime.

    # ------------------------------------------------------------------------------------------------------------------

    # Negativne quantity vrednosti


    print(df_order_items[df_order_items["quantity"] < 0])

    print(df_orders[df_orders["order_id"] == 15012])
    print(df_products[df_products["product_id"] == 101])

    # order_item_id = 67 ima quantity = -3.
    # Nije moguce pouzdano utvrditi ispravnu vrednost,
    # pa se zapis uklanja tokom ciscenja.

    # ------------------------------------------------------------------------------------------------------------------

    # Cene manje ili jednake nuli

    print(df_products[df_products["price"] <= 0])
    print(df_order_items[df_order_items["product_id"] == 121])

    # product_id = 121 ima price = 0 i naziv "Broken Product".
    # Proizvod i povezana stavka bice uklonjeni.

    # ------------------------------------------------------------------------------------------------------------------

    # Da li je negde cost > price?

    print(df_products[df_products["cost"] > df_products["price"]])
    print(df_order_items[df_order_items["product_id"] == 122])

    # product_id = 122 ima cost veci od price.
    # Proizvod i povezana stavka bice uklonjeni.
    # Porudzbina 15020 ostaje jer sadrzi druge validne stavke.

    # ------------------------------------------------------------------------------------------------------------------

    # Nepostojeci customer ID-jevi

    print(
        df_orders[
            ~df_orders["customer_id"].isin(df_customers["customer_id"])
        ]
    )

    print(df_order_items[df_order_items["order_id"] == 15032])

    # order_id = 15032 pripada customer_id = 8888,
    # koji ne postoji u customers tabeli.

    # ------------------------------------------------------------------------------------------------------------------

    # Nepostojeci product ID-jevi

    print(
        df_order_items[
            ~df_order_items["product_id"].isin(df_products["product_id"])
        ]
    )

    print(df_order_items[df_order_items["order_id"] == 15010])

    # order_item_id = 66 sadrzi product_id = 999,
    # koji ne postoji u products tabeli.

    # ------------------------------------------------------------------------------------------------------------------

    # Neispravni datumi

    print(
        "\n// Neispravni datumi u tabeli 'df_customers':\n\n",
        df_customers[
            pd.to_datetime(
                df_customers["registration_date"],
                errors="coerce"
            ).isna()
        ]
    )

    print(
        "\n// Neispravni datum u tabeli 'df_orders':\n\n",
        df_orders[
            pd.to_datetime(
                df_orders["order_date"],
                errors="coerce"
            ).isna()
        ]
    )

    # Neispravni datumi ce tokom ciscenja biti konvertovani u NaT.

    # ------------------------------------------------------------------------------------------------------------------

    # Sumnjivi kupci

    print(
        df_customers[
            df_customers["first_name"].str.contains(
                "test|ghost",
                case=False,
                na=False
            )
        ]
    )


def clean_data(df_customers, df_products, df_orders, df_order_items):
    print("\n================================ 3. CISCENJE ================================\n")

    df_customers_clean = df_customers.copy()
    df_products_clean = df_products.copy()
    df_orders_clean = df_orders.copy()
    df_order_items_clean = df_order_items.copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje testnih customer-a

    df_customers_clean = df_customers_clean[
        ~df_customers_clean["first_name"].str.contains(
            "test|ghost",
            case=False,
            na=False
        )
    ].copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje dupliranih customer-a prema email adresi

    df_customers_clean = df_customers_clean.drop_duplicates(
        subset=["email"],
        keep="first"
    ).copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje proizvoda sa nevalidnim price/cost vrednostima

    df_products_clean = df_products_clean[
        (df_products_clean["price"] > 0) &
        (df_products_clean["cost"] <= df_products_clean["price"])
    ].copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje duplikata iz orders tabele

    df_orders_clean = df_orders_clean.drop_duplicates().copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje porudzbina koje pripadaju nepostojecim customer-ima

    df_orders_clean = df_orders_clean[
        df_orders_clean["customer_id"].isin(df_customers_clean["customer_id"])
    ].copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje nevalidnih stavki porudzbina

    df_order_items_clean = df_order_items_clean[
        df_order_items_clean["product_id"].isin(df_products_clean["product_id"])
    ].copy()

    df_order_items_clean = df_order_items_clean[
        df_order_items_clean["order_id"].isin(df_orders_clean["order_id"])
    ].copy()

    df_order_items_clean = df_order_items_clean[
        df_order_items_clean["quantity"] > 0
    ].copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Uklanjanje dupliranih stavki porudzbina

    df_order_items_clean = df_order_items_clean.drop_duplicates(
        subset=["order_id", "product_id", "quantity"],
        keep="first"
    ).copy()

    # ------------------------------------------------------------------------------------------------------------------

    # Konverzija datuma

    df_customers_clean["registration_date"] = pd.to_datetime(
        df_customers_clean["registration_date"],
        errors="coerce"
    )

    df_orders_clean["order_date"] = pd.to_datetime(
        df_orders_clean["order_date"],
        errors="coerce"
    )

    # ------------------------------------------------------------------------------------------------------------------

    # Standardizacija country vrednosti

    df_customers_clean["country"] = df_customers_clean["country"].str.capitalize()

    # ------------------------------------------------------------------------------------------------------------------

    # Provera ociscenih podataka

    print(df_customers_clean.dtypes)
    print(df_orders_clean.dtypes)
    print(df_customers_clean["country"].value_counts())

    # ------------------------------------------------------------------------------------------------------------------

    # Cuvanje ociscenih podataka

    df_customers_clean.to_csv(OUTPUT / "customers_clean.csv", index=False)
    df_products_clean.to_csv(OUTPUT / "products_clean.csv", index=False)
    df_orders_clean.to_csv(OUTPUT / "orders_clean.csv", index=False)
    df_order_items_clean.to_csv(OUTPUT / "order_items_clean.csv", index=False)

    return df_customers_clean, df_products_clean, df_orders_clean, df_order_items_clean


def merge_data(df_customers_clean, df_products_clean, df_orders_clean, df_order_items_clean):
    print("\n================================ 4. SPAJANJE PODATAKA ================================\n")

    df_customers_orders = pd.merge(
        df_customers_clean,
        df_orders_clean,
        on="customer_id",
        how="inner"
    )

    df_products_items = pd.merge(
        df_products_clean,
        df_order_items_clean,
        on="product_id",
        how="inner"
    )

    df_joined = pd.merge(
        df_customers_orders,
        df_products_items,
        on="order_id",
        how="inner"
    )

    # ------------------------------------------------------------------------------------------------------------------

    # Provera spojenog DataFrame-a

    print(df_joined.shape)
    print(df_joined.columns.tolist())
    print("Broj duplikata:", df_joined.duplicated().sum())
    print("Missing values:")
    print(df_joined.isna().sum())

    # Jedini ocekivani missing podatak je NaT za prethodno detektovan
    # neispravan order_date.

    print(df_joined[df_joined.isna().any(axis=1)])

    return df_joined


def calculate_financial_metrics(df_joined):
    print("\n================================ 5. REVENUE I PROFIT ================================\n")

    # ------------------------------------------------------------------------------------------------------------------

    # Metrike: revenue, total_cost, profit, profit_margin

    df_joined = df_joined.copy()

    df_joined["revenue"] = (
        df_joined["price"] * df_joined["quantity"]
    ) * (1 - df_joined["discount"])

    df_joined["total_cost"] = df_joined["cost"] * df_joined["quantity"]

    df_joined["profit"] = df_joined["revenue"] - df_joined["total_cost"]

    df_joined["profit_margin"] = np.where(
        df_joined["revenue"] != 0,
        df_joined["profit"] / df_joined["revenue"].replace(0, np.nan),
        np.nan
    )

    print(df_joined)

    # ------------------------------------------------------------------------------------------------------------------

    # Redosled kolona u finalnom datasetu

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
    ]

    # ------------------------------------------------------------------------------------------------------------------

    # Ukupne metrike

    final_revenue = df_joined["revenue"].sum()
    final_cost = df_joined["total_cost"].sum()
    final_profit = df_joined["profit"].sum()

    final_profit_margin = (
        final_profit / final_revenue
        if final_revenue != 0
        else np.nan
    )

    total_orders = df_joined["order_id"].nunique()

    average_order_value = (
        final_revenue / total_orders
        if total_orders != 0
        else np.nan
    )

    print(f"Ukupni revenue: {final_revenue:.2f}")
    print(f"Ukupni cost: {final_cost:.2f}")
    print(f"Ukupni profit: {final_profit:.2f}")
    print(f"Ukupna profitna margina: {final_profit_margin * 100:.2f}%")
    print(f"Prosecna vrednost porudzbine: {average_order_value:.2f}")

    # ------------------------------------------------------------------------------------------------------------------

    # Cuvanje finalnog dataseta spremnog za analizu

    df_joined.to_csv(OUTPUT / "sales_clean.csv", index=False)

    return df_joined


def find_max(series):
    valid_series = series.dropna()

    if valid_series.empty:
        return None, None

    return valid_series.idxmax(), valid_series.max()


def analyze_sales(df_joined):
    print("\n================================ 6. ANALIZA PRODAJE ================================\n")

    # ------------------------------------------------------------------------------------------------------------------

    # Osnovna analiza

    total_orders = df_joined["order_id"].nunique()
    unique_customers = df_joined["customer_id"].nunique()
    total_sold_products = df_joined["quantity"].sum()

    final_revenue = df_joined["revenue"].sum()
    final_profit = df_joined["profit"].sum()

    print(f"Ukupan broj porudzbina: {total_orders}")
    print(f"Broj jedinstvenih kupaca: {unique_customers}")
    print(f"Ukupan broj prodatih proizvoda: {total_sold_products}")
    print(f"Ukupan revenue: {final_revenue:.2f}")
    print(f"Ukupan profit: {final_profit:.2f}")

    # ------------------------------------------------------------------------------------------------------------------

    # Analiza proizvoda:


    # Najprodavaniji proizvod po kolicini

    quantity_by_product = df_joined.groupby("product_name")["quantity"].sum()

    top_quantity_product, highest_product_quantity = find_max(quantity_by_product)

    if highest_product_quantity is not None:
        print(
            f"Najprodavaniji proizvod je {top_quantity_product} "
            f"sa {highest_product_quantity} prodatih jedinica."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Proizvod sa najvecim revenue

    revenue_by_product = df_joined.groupby("product_name")["revenue"].sum()

    top_revenue_product, highest_product_revenue = find_max(revenue_by_product)

    if highest_product_revenue is not None:
        print(
            f"Proizvod sa najvećim revenue je {top_revenue_product} "
            f"sa revenue od {highest_product_revenue:.2f}."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Proizvod sa najvecim profitom

    profit_by_product = df_joined.groupby("product_name")["profit"].sum()

    top_profit_product, highest_product_profit = find_max(profit_by_product)

    if highest_product_profit is not None:
        print(
            f"Proizvod sa najvecim profitom je {top_profit_product} "
            f"sa profitom od {highest_product_profit:.2f}."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Proizvod sa najvecom profitnom marginom

    profit_margin_by_product = (
        profit_by_product / revenue_by_product.replace(0, np.nan)
    )

    top_margin_product, highest_product_margin = find_max(profit_margin_by_product)

    if highest_product_margin is not None:
        print(
            f"Proizvod sa najvecom profitnom marginom je "
            f"{top_margin_product} sa marginom od "
            f"{highest_product_margin * 100:.2f}%."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Analiza kategorija

    revenue_by_category = df_joined.groupby("category")["revenue"].sum()
    profit_by_category = df_joined.groupby("category")["profit"].sum()

    profit_margin_by_category = (
        profit_by_category / revenue_by_category.replace(0, np.nan)
    )

    # ------------------------------------------------------------------------------------------------------------------

    # Kategorija sa najvecim revenue

    top_revenue_category, highest_category_revenue = find_max(revenue_by_category)

    if highest_category_revenue is not None:
        print(
            f"Kategorija sa najvecim revenue je {top_revenue_category} "
            f"sa revenue od {highest_category_revenue:.2f}."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Kategorija sa najvecim profitom

    top_profit_category, highest_category_profit = find_max(profit_by_category)

    if highest_category_profit is not None:
        print(
            f"Kategorija sa najvecim profitom je {top_profit_category} "
            f"sa profitom od {highest_category_profit:.2f}."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Kategorija sa najvecom profitnom marginom

    top_margin_category, highest_category_margin = find_max(profit_margin_by_category)

    if highest_category_margin is not None:
        print(
            f"Kategorija sa najvecom profitnom marginom je "
            f"{top_margin_category} sa marginom od "
            f"{highest_category_margin * 100:.2f}%."
        )
    else:
        print("Nema validnih podataka za analizu.")


def analyze_customers(df_joined):
    print("\n================================ 7. CUSTOMER ANALYSIS ================================\n")

    # ------------------------------------------------------------------------------------------------------------------

    # Top 10 kupaca po potrosnji

    df_joined = df_joined.copy()

    df_joined["Customer"] = (
        df_joined["first_name"] + " " + df_joined["last_name"]
    )

    customers_analysis = df_joined.groupby(
        ["customer_id", "Customer"]
    ).agg(
        Orders=("order_id", "nunique"),
        Revenue=("revenue", "sum"),
        Profit=("profit", "sum")
    )

    top10_customers = customers_analysis.nlargest(10, "Revenue")

    print(top10_customers)

    # ------------------------------------------------------------------------------------------------------------------

    # Kupac sa najvise porudzbina

    top_orders_customer, highest_customer_orders = find_max(customers_analysis["Orders"])

    if highest_customer_orders is not None:
        print(
            f"{top_orders_customer[1]} ima najvise porudzbina - "
            f"{highest_customer_orders} porudzbina."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Kupac sa najvecom potrosnjom

    top_revenue_customer, highest_customer_revenue = find_max(customers_analysis["Revenue"])

    if highest_customer_revenue is not None:
        print(
            f"{top_revenue_customer[1]} je najvise potrosio - "
            f"{highest_customer_revenue:.2f}."
        )
    else:
        print("Nema validnih podataka za analizu.")

    # ------------------------------------------------------------------------------------------------------------------

    # Kupac koji donosi najveci profit

    top_profit_customer, highest_customer_profit = find_max(customers_analysis["Profit"])

    if highest_customer_profit is not None:
        print(
            f"{top_profit_customer[1]} donosi najveci profit "
            f"u iznosu od {highest_customer_profit:.2f}."
        )
    else:
        print("Nema validnih podataka za analizu.")




def main():

    df_customers, df_products, df_orders, df_order_items = load_data()

    check_data_quality(
        df_customers,
        df_products,
        df_orders,
        df_order_items
    )

    df_customers_clean, df_products_clean, df_orders_clean, df_order_items_clean = clean_data(
        df_customers,
        df_products,
        df_orders,
        df_order_items
    )

    df_joined = merge_data(
        df_customers_clean,
        df_products_clean,
        df_orders_clean,
        df_order_items_clean
    )

    df_joined = calculate_financial_metrics(df_joined)

    analyze_sales(df_joined)

    analyze_customers(df_joined)


if __name__ == "__main__":
    main()
