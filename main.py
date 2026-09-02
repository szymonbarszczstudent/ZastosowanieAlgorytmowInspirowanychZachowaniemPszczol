from eksperymenty.uruchom import uruchom_eksperymenty
def main():
    katalog_wyjscia = uruchom_eksperymenty()
    print(f"Wyniki zapisano w: {katalog_wyjscia}")
if __name__ == '__main__':
    main()
