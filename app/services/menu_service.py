from app.models import Menu
from app import db

class MenuService:
    @staticmethod
    def create_menu(data):
        """Creates a new menu for a mess."""
        try:
            new_menu = Menu(
                menu_id=data['menu_id'],
                mess_id=data['mess_id'],
                menu_name=data['menu_name'],
                menu_description=data['menu_description'],
                price=data['price']
            )
            db.session.add(new_menu)
            db.session.commit()
            return {"message": "Menu created successfully", "status": 200}, 200
        except Exception as e:
            return {"message": str(e), "status": 500}, 500

    @staticmethod
    def update_menu(menu_id, data):
        """Updates a menu by menu_id."""
        try:
            menu = Menu.query.filter_by(menu_id=menu_id).first()
            if not menu:
                return {"message": "Menu not found", "status": 404}, 404

            menu.menu_name = data.get('menu_name', menu.menu_name)
            menu.menu_description = data.get('menu_description', menu.menu_description)
            menu.price = data.get('price', menu.price)
            db.session.commit()

            return {"message": "Menu updated successfully", "status": 200}, 200
        except Exception as e:
            return {"message": str(e), "status": 500}, 500

    @staticmethod
    def delete_menu(menu_id):
        """Deletes a menu by menu_id."""
        try:
            menu = Menu.query.filter_by(menu_id=menu_id).first()
            if not menu:
                return {"message": "Menu not found", "status": 404}, 404

            db.session.delete(menu)
            db.session.commit()
            return {"message": "Menu deleted successfully", "status": 200}, 200
        except Exception as e:
            return {"message": str(e), "status": 500}, 500

    @staticmethod
    def get_all_menus(mess_id):
        """Fetches all menus for the provided mess_id."""
        try:
            menus = Menu.query.filter_by(mess_id=mess_id).all()
            if not menus:
                return {"message": "No menus found for the provided mess ID", "status": 404}, 404
            
            return {"menus": [menu.to_dict() for menu in menus], "status": 200}, 200
        except Exception as e:
            return {"message": str(e), "status": 500}, 500
