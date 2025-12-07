from JSON_Extractor.JSON_Extractor import get_product_data


if __name__ == "__main__":
    print('Вставьте/Введите ссылка на продукт на сайте Nintendo\nПример ссылки: https://www.nintendo.com/us/store/products/sword-of-the-vagrant-switch/')

    while True:
        url = input('Ссылка: ')

        if not url or url.strip() == '':
            print(
                '\nВнимание: Вы не передали ссылку продукта. Будет использована ссылка из примера\n')

            url = 'https://www.nintendo.com/us/store/products/sword-of-the-vagrant-switch'


        if 'www.nintendo.com' not in url:
            print(
                '\nВнимание: Ссылка не ведет на сайт nintento. Повторите ввод\n')

            continue


        if ' ' in url:
            print('\nВ ссылку обнаружены пустые строки, они были успешно удалены \n')
            url = url.replace(" ", "")

        break

    print('Ваша ссылка: ' + url)

    print('Процесс выгрузки данных запущен. Ожидайте...')

    # Загружка данных с сайта Nintendo
    get_product_data(url)

    print('Процесс успешно завершен!')