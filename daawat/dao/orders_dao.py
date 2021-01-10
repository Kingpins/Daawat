from daawat.util.cql_file_util import get_cql_schema_string_from_file
from daawat.util.data_type_util import uuid_from_string
from daawat.model.order import Orders

class OrdersDAO(object):

    table_name = "orders"

    create_stmt = get_cql_schema_string_from_file(table_name)

    insert_stmt = 'INSERT INTO {table_name} (hotel_id,customer_id,order_id,product,time_of_order,price,quantity,status) ' \
                  'VALUES (:hotel_id,:customer_id,:order_id,:product,:time_of_order,:price,:quantity,:status);'.format(table_name=table_name)

    select_all_orders = 'SELECT * FROM {table_name} WHERE hotel_id = :hotel_id AND customer_id = :customer_id ALLOW FILTERING;'.format(table_name=table_name)

    update_status = 'UPDATE {table_name} SET status = :status WHERE hotel_id = :hotel_id AND customer_id = :customer_id AND order_id = :order_id AND time_of_order = :time_of_order' \
                                              ''.format(table_name=table_name)                                                                                                                               

    def __init__(self, _session):
        self._session = _session
        self.maybe_create_schema()
        self.insert_prep_stmt = _session.prepare(self.insert_stmt)
        self.select_all_orders_prep_stmt = _session.prepare(self.select_all_orders)
        self.update_status_prep_stmt = _session.prepare(self.update_status)
    
    def maybe_create_schema(self):
        self._session.execute(self.create_stmt)

    def create_order(self, order):
        def handle_success(results):
            print("order added")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)

        insert_future = self._session.execute_async(self.insert_prep_stmt.bind({
            'hotel_id':order.hotel_id,
            'customer_id':order.customer_id,
            'order_id':order.order_id,
            'product':order.product_id,
            'time_of_order':order.time_of_order,
            'price':order.price,
            'quantity':order.quantity,
            'status':False,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    def update_order_status(self, hotel_id,customer_id,order_id,time_of_order):
        def handle_success(results):
            print("order updated")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)

        insert_future = self._session.execute_async(self.update_status_prep_stmt.bind({
            'hotel_id':hotel_id,
            'customer_id':customer_id,
            'order_id':order_id,
            'status':True,
            'time_of_order':time_of_order,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    
    def get_orders(self,hotel_id,customer_id):
        orders = []

        if len(customer_id) == 1:
            result = self._session.execute(self.select_all_orders_prep_stmt.bind({
                'hotel_id': hotel_id,
                'customer_id':customer_id[0]}
            ))

            return result
        
        for customer in customer_id:
            result = self._session.execute(self.select_all_orders_prep_stmt.bind({
                'hotel_id': hotel_id,
                'customer_id':customer}
            ))
            for order in result:
                orders.append(order)
        return orders
    