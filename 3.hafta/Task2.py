# Verilen bir listedeki tüm elemanları recursive olarak düzleştiren (flatten) bir program yazın.
# Liste iç içe listeler içerebilir.
# Gereksinimler:
# - Recursive lambda kullanın (Y-combinator)
# - Map/filter ile implemente edin
# - Sadece sayıları koruyun, diğer tipleri filtreleyin
# Örnek: [1, [2, [3, 4]], 5, [6, 'a']] → [1, 2, 3, 4, 5, 6]

mixed_list = [1, [2, [3, 4]], 5, [6, 'a'], [[7, 8], [9, [10]]], 'hello', 11.5]

flatten = (lambda f: (lambda x: f(f, x)))(
    lambda self, lst: sum(
        map(
            lambda el: self(self, el) if isinstance(el, list)
                       else [el] if isinstance(el, (int, float))
                       else [],
            lst
        ),
        []
    )
)
flattened_list = flatten(mixed_list)
print("Flattened list (only numbers):", flattened_list)