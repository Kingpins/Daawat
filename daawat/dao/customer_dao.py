from daawat.util.cql_file_util import get_cql_schema_string_from_file
from daawat.util.data_type_util import uuid_from_string
from daawat.model.customer import Customers

# Data Access Object for the 'customers' database table
# Contains CQL Statements and DataStax Driver APIs for reading and writing from the database
class CustomersDAO(object):

    table_name = "customers"

    create_stmt = get_cql_schema_string_from_file(table_name)

    insert_stmt = 'INSERT INTO {table_name} (customer_id,customer_name,status,hotel_id,table_no) ' \
                  'VALUES (:customer_id,:customer_name,:status,:hotel_id,:table_no);'.format(table_name=table_name)

    select_all_customer_for_hotel = 'SELECT * FROM {table_name} WHERE hotel_id = :hotel_id ALLOW FILTERING;' \
                                              ''.format(table_name=table_name)

    select_customer_status_for_customer_id = 'SELECT status FROM {table_name} WHERE customer_id = :customer_id ALLOW FILTERING;' \
                                              ''.format(table_name=table_name)
    update_status_for_customer_id = 'UPDATE {table_name} SET status = True WHERE customer_id = :customer_id ' \
                                              ''.format(table_name=table_name)                                                                                                                                                                             
    delete_customer_by_customer_id =  'DELETE FROM {table_name}  WHERE customer_id = :customer_id ' \
                                              ''.format(table_name=table_name)       
    select_customer_for_customer_id = 'SELECT * FROM {table_name} WHERE customer_id = :customer_id ;' \
                                              ''.format(table_name=table_name)

    def __init__(self, _session):
        self._session = _session
        self.maybe_create_schema()
        self.insert_prep_stmt = _session.prepare(self.insert_stmt)
        self.select_all_customer_for_hotel_prep_stmt = _session.prepare(self.select_all_customer_for_hotel)
        self.select_customer_status_for_customer_id_prep_stmt = _session.prepare(self.select_customer_status_for_customer_id)
        self.update_status_for_customer_id_prep_stmt = _session.prepare(self.update_status_for_customer_id)
        self.delete_customer_by_customer_id_prep_stmt = _session.prepare(self.delete_customer_by_customer_id)
        self.select_customer_for_customer_id_prep_stmt = _session.prepare(self.select_customer_for_customer_id)
    def maybe_create_schema(self):
        self._session.execute(self.create_stmt)

    def create_customer(self, customer):
        # We use the DataStax Driver's Async API here to write the rows to the database in a non-blocking fashion
        
        def handle_success(results):
            print("customer added")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)


        insert_future = self._session.execute_async(self.insert_prep_stmt.bind({
            'customer_id':customer.customer_id,
            'customer_name':customer.customer_name,
            'status':customer.status,
            'hotel_id':customer.hotel_id,
            'table_no':customer.table_no,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    def update_customer(self, customer_id):
        # We use the DataStax Driver's Async API here to update the rows to the database in a non-blocking fashion
        def handle_success(results):
            print("customer updated")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)

        update_future = self._session.execute_async(self.update_status_for_customer_id_prep_stmt.bind({
            'customer_id':customer_id
        }))

        update_future.add_callbacks(handle_success, handle_error)

    def delete_customer(self,customer_id):
        delete_result = self._session.execute(self.delete_customer_by_customer_id_prep_stmt.bind({
            'customer_id': customer_id}
        ))
        return True

    def get_customer_by_hotel_id(self,hotel_id):
        result = self._session.execute(self.select_all_customer_for_hotel_prep_stmt.bind({
            'hotel_id': hotel_id}
        ))
        return result

    def get_customer_by_customer_id(self,customer_id):
        result = self._session.execute(self.select_customer_for_customer_id_prep_stmt.bind({
            'customer_id': customer_id}
        ))
        return result

    def get_customer_status_by_customer_id(self,customer_id):
        result = self._session.execute(self.select_customer_status_for_customer_id_prep_stmt.bind({
            'customer_id': customer_id}
        ))
        return result
