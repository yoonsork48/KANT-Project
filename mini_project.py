# ========== 상품 클래스 ============= == == == == == = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class Product:
    next_number = 1                                                 # 상품마다 번호를 매김

    def __init__(self, name, price, qty):                           # 상품의 객체화, 구성 및 정의
        if price < 0 or qty < 0:                                    # 상품의 가격이나 갯수가 0보다 적을때
            print("가격과 재고는 음수일 수 없습니다.")              # 0보다 낮은 수 발생시 출력문구
            return                                                  # 및 되돌아감

        self.number = Product.next_number                           # 상품 번호 자동부여
        Product.next_number += 1                                    # 다음에 생성될 상품을 위해 클래스 변수의 값을 1 증가시킴.

        self.name = name                                            # 상품명을 상품 객체에 저장
        self.price = price                                          # 상품가격을 상품 객체에 저장
        self.__qty = qty                                            # 상품갯수를 상품 객체에 저장

    def decrease_stock(self,qty):                                   # 실제 재고 감소

        if qty <= 0 or qty > self.__qty:                            # 재고보다 많이 빼거나 잘못된 수량이면 거절
            return False

        self.__qty -= qty                                           # 재고 차감

        return True                                                 # 정상 작동

    def get_qty(self):                                              # 상품 실시간 재고 조회 가능
        return self.__qty


# ========== 장바구니 클래스 ============= == == == == == = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class ShoppingCart:

    def __init__(self):                                             # 장바구니 생성
        self.bucket = {}                                            # 장바구니 비워진 상태

    # 장바구니에 추가 구현
    def add(self, number, qty, products):
        product = products.get(number)                              # 숫자(상품번호) 입력
        if product is None:                                         # 없는 상품번호일때
            print("존재하지 않는 상품입니다.")
            return
        if qty <= 0:                                                # 담을 상품의 갯수가 0보다 작거나 같을때(오류입력시)
            print("수량은 1개 이상이어야 합니다.")
            return
        if product.get_qty() == 0:                                  # 품절 : 실제 재고가 0일때, 즉 담은 상품의 반환값이 0일때
            print("품절입니다.")
            return

        current = self.bucket.get(number, 0)                        # 장바구니에 담긴 상품
        available = product.get_qty() - current                     # 더 담을 수 있는 물건 갯수(남은 재고)
        if qty > available:                                         # 담고싶은 갯수가 남은 재고보다 많을때
            print(f"재고가 부족합니다. 추가 가능 수량: {available}개")
            return

        self.bucket[number] = current + qty                         # 장바구니에 정상적으로 더 갯수가 추가 되면
        print(f"{product.name} {qty}개를 담았습니다.")

    # 장바구니로부터 빼기 구현
    def remove(self, number, qty, products):
        if number not in self.bucket:                               # 없는데 빼려고 하면
            print("장바구니에 없는 상품입니다.")
            return
        if qty <= 0:                                                # 뺄 갯수가 0과 같거나 적으면
            print("수량은 1개 이상이어야 합니다.")
            return

        current = self.bucket[number]                               # 장바구니에 담긴 상품
        if qty > current:                                           # 뺄 수량이 장바구니 안의 물건보다 많을때 못하게 하기
            print(f"담긴 수량이 부족합니다. 현재 {current}개")
            return

        self.bucket[number] -= qty                                  # 장바구니에서 제거할 수량 빼기
        if self.bucket[number] == 0:                                # 장바구니에서 제거되면 해당 상품번호 딕셔너리에서 삭제
            del self.bucket[number]
        print(f"{products[number].name} {qty}개를 뺐습니다.")

    def subtotal(self, products):                                   # 장바구니에 남은 물건 계산
        total = 0                                                   # 누적 합계 초기하
        for number, qty in self.bucket.items():                     # 장바구니 상품을 하나씩 순회
            product = products[number]                              # 상품 번호로 상품 객체를 조회
            total += product.price * qty                            # 가격 x 수량을 합계에 더함
        return total    

    def show(self, products):                                       # 장바구니 현황 보여주기
        if not self.bucket:                                         # 딕셔너리가 비어있는지 확인.
            print("장바구니가 비어 있습니다.")                      # 비어있다면 해당 메시지 출력후 종료
            return

        print("\n" + "-" * 45)
        print("[장바구니]")
        for number, qty in self.bucket.items():                     # 담긴 상품들의 정보 조회 및 소계 계산
            product = products[number]                              #   - 상품명
            price = product.price * qty                             #   - 상품의 소계(가격x갯수)
            print(f"{number}. {product.name:<12} x {qty:<3} {price:>10,}원")    # 출력물(왼쪽 정렬, 최소12칸/왼쪽 정렬, 최소3칸/오른쪽 정렬, 최소 10칸, 천 단위 쉼표)
        print("-" * 45)
        print(f"총 상품 금액: {self.subtotal(products):,}원")       #  - 총 금액( 기존 메서드 재사용에 의의)

    def checkout(self, products):
        if not self.bucket:
            print("장바구니가 비어 있어 결제할 수 없습니다.")
            return False

        # 모든 상품을 검증한 후에만 재고를 변경한다.
        for number, qty in self.bucket.items():
            product = products.get(number)
            if product is None:
                print(f"상품 번호 {number}를 찾을 수 없어 결제를 중단합니다.")
                return False
            if qty <= 0 or qty > product.get_qty():
                print(f"{product.name}의 재고가 부족하거나 수량이 잘못되었습니다.")
                return False

        total = self.subtotal(products)
        print("\n========== 영수증 ==========")
        for number, qty in self.bucket.items():
            product = products[number]
            print(f"{product.name:<12} x {qty:<3} {product.price * qty:>10,}원")
        print("-" * 45)
        print(f"결제 금액: {total:,}원")

        for number, qty in self.bucket.items():
            products[number].decrease_stock(qty)
        self.bucket.clear()
        print("결제가 완료되었습니다. 장바구니를 초기화했습니다.")
        return True

# ========== 쇼핑몰 클래스 ============= == == == == == = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
class ShoppingMall:
    def __init__(self):
        self.product_list = [
            Product("무선 이어폰", 89000, 3),
            Product("텀블러", 15000, 10),
            Product("보조배터리", 32000, 5),
            Product("마우스패드", 9000, 0),
            Product("USB 허브", 18000, 4),
        ]

        # 번호를 키로 저장하여 빠르게 조회한다.
        self.products = {}
        for product in self.product_list:
            self.products[product.number] = product
        self.cart = ShoppingCart()

    def show_products(self):
        print("\n<<<<<<<<<<<<<<< 상품 목록 >>>>>>>>>>>>>>>>>")
        for number, product in self.products.items():
            # 실제 재고에서 현재 장바구니에 담긴 수량을 제외
            # 결제 전에는 상품의 실제 재고를 바꾸지 않음
            cart_qty = self.cart.bucket.get(number, 0)
            available = product.get_qty() - cart_qty
            stock = "품절" if available == 0 else f"재고 {available}개"
            print(f"{number}. {product.name:<12} {product.price:>8,}원 ({stock})")

    def get_number(self, message):
        try:
            return int(input(message))
        except ValueError:
            print("숫자를 제대로 입력해주세요.")
            return None

    # ========== 쇼핑몰 사이트 구동 ===========
    def run(self):
        while True:
            print("\n" + "-" * 56)
            print("1.상품목록 2.담기 3.빼기 4.장바구니 5.결제 q.종료")
            print("-" * 56)
            user_input = input("선택: ").strip().lower()

            if user_input == "1":
                self.show_products()
            elif user_input == "2":
                number = self.get_number("상품 번호: ")
                if number is None:
                    continue
                if number not in self.products:
                    print("존재하지 않는 상품입니다.")
                    continue
                qty = self.get_number("수량: ")
                if qty is not None:
                    self.cart.add(number, qty, self.products)
            elif user_input == "3":
                number = self.get_number("상품 번호: ")
                if number is None:
                    continue
                qty = self.get_number("뺄 수량: ")
                if qty is not None:
                    self.cart.remove(number, qty, self.products)
            elif user_input == "4":
                self.cart.show(self.products)
            elif user_input == "5":
                self.cart.checkout(self.products)
            elif user_input == "q":
                print("쇼핑몰을 종료합니다.")
                break
            else:
                print("다시 선택해 주세요.")


if __name__ == "__main__":
    mall = ShoppingMall()
    mall.run()
