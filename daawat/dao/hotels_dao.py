from daawat.util.cql_file_util import get_cql_schema_string_from_file
from daawat.util.data_type_util import uuid_from_string
from daawat.model.hotels import Hotels


# Data Access Object for the 'hotels' database table
# Contains CQL Statements and DataStax Driver APIs for reading and writing from the database
class HotelsDAO(object):

    table_name = "hotels"

    create_stmt = get_cql_schema_string_from_file(table_name)

    insert_stmt = 'INSERT INTO {table_name} (hotel_id, hotel_name,hotel_bio,hotel_address,hotel_phone,hotel_tables,hotel_logo,useremail) ' \
                  'VALUES (:hotel_id,:hotel_name,:hotel_bio,:hotel_address,:hotel_phone,:hotel_tables,:hotel_logo,:useremail);'.format(table_name=table_name)

    select_all_hotels_for_email = 'SELECT * FROM {table_name} WHERE useremail = :useremail ALLOW FILTERING;' \
                                              ''.format(table_name=table_name)
    select_hotels_for_hotel_id = 'SELECT * FROM {table_name} WHERE hotel_id = :hotel_id ALLOW FILTERING;' \
                                              ''.format(table_name=table_name)

    def __init__(self, _session):
        self._session = _session
        self.maybe_create_schema()
        self.insert_prep_stmt = _session.prepare(self.insert_stmt)
        self.select_all_for_hotel_prep_stmt = _session.prepare(self.select_all_hotels_for_email)
        self.select_hotels_for_hotel_id_prep_stmt = _session.prepare(self.select_hotels_for_hotel_id)
        

    def maybe_create_schema(self):
        self._session.execute(self.create_stmt)

    def create_hotel(self, hotel):
        # We use the DataStax Driver's Async API here to write the rows to the database in a non-blocking fashion
        
        def handle_success(results):
            print("hotel added")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)


        insert_future = self._session.execute_async(self.insert_prep_stmt.bind({
            'hotel_id':hotel.hotel_id,
            'hotel_name': hotel.hotel_name,
            'hotel_bio': hotel.hotel_bio,
            'hotel_address': hotel.hotel_address,
            'hotel_phone': hotel.hotel_phone,
            'hotel_tables' : hotel.hotel_tables,
            'hotel_logo':hotel.hotel_logo,
            'useremail':hotel.userEmail,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    def get_hotel_exits(self,email):
        count = 0
        result = self._session.execute(self.select_all_for_hotel_prep_stmt.bind({
            'useremail': email}
        ))
        for row in result:
            count += 1
        if count == 1:
            return True
        else:
            return False

    def get_hotel_exits_by_hotel_id(self,hotel_id):
        count = 0
        result = self._session.execute(self.select_hotels_for_hotel_id_prep_stmt.bind({
            'hotel_id': hotel_id}
        ))
        for row in result:
            count += 1
        if count == 1:
            return True
        else:
            return False
            
    def get_hotel_by_email(self,email):
        result = self._session.execute(self.select_all_for_hotel_prep_stmt.bind({
            'useremail': email}
        ))
        return result

    
    def get_hotel_by_hotel_id(self,hotel_id):
        result = self._session.execute(self.select_hotels_for_hotel_id_prep_stmt.bind({
            'hotel_id': hotel_id}
        ))
        return result
