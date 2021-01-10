from daawat.util.cql_file_util import get_cql_schema_string_from_file
from daawat.util.data_type_util import uuid_from_string
from daawat.model.users import Users

# Data Access Object for the 'users' database table
# Contains CQL Statements and DataStax Driver APIs for reading and writing from the database
class UsersDAO(object):

    table_name = "users"

    create_stmt = get_cql_schema_string_from_file(table_name)

    insert_stmt = 'INSERT INTO {table_name} (first_name,last_name,phone,email,password) ' \
                  'VALUES (:first_name,:last_name,:phone,:email,:password);'.format(table_name=table_name)

    select_all_users_for_email = 'SELECT * FROM {table_name} WHERE email = :email;' \
                                              ''.format(table_name=table_name)

    def __init__(self, _session):
        self._session = _session
        self.maybe_create_schema()
        self.insert_prep_stmt = _session.prepare(self.insert_stmt)
        self.select_all_for_email_prep_stmt = _session.prepare(self.select_all_users_for_email)

    def maybe_create_schema(self):
        self._session.execute(self.create_stmt)

    def create_user(self, first_name,last_name,phone,email,password):
        # We use the DataStax Driver's Async API here to write the rows to the database in a non-blocking fashion

        def handle_success(results):
            print("added")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)

    
        this_user = Users(first_name,last_name,phone,email,password)

        insert_future = self._session.execute_async(self.insert_prep_stmt.bind({
            'first_name': this_user.first_name,
            'last_name': this_user.last_name,
            'phone': this_user.phone,
            'email': this_user.email,
            'password': this_user.password,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    def get_user_exits(self,email):
        count = 0
        result = self._session.execute(self.select_all_for_email_prep_stmt.bind({
            'email': email}
        ))
        for row in result:
            count += 1
        if count == 1:
            return True
        else:
            return False

    def get_user_by_email(self,email):
        result = self._session.execute(self.select_all_for_email_prep_stmt.bind({
            'email': email}
        ))
        return result
