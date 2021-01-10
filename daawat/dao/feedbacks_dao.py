from daawat.util.cql_file_util import get_cql_schema_string_from_file
from daawat.util.data_type_util import uuid_from_string
from daawat.model.inovice import Invoices

class FeedbacksDAO(object):

    table_name = "feedbacks"

    create_stmt = get_cql_schema_string_from_file(table_name)

    insert_stmt = 'INSERT INTO {table_name} (hotel_id,customer_id,customer_name,ratings,feedback_comment,time_of_feedback) ' \
                  'VALUES (:hotel_id,:customer_id,:customer_name,:ratings,:feedback_comment,:time_of_feedback);'.format(table_name=table_name)

    select_all_feedbacks_for_hotel_id = 'SELECT * FROM {table_name} WHERE hotel_id = :hotel_id ;'.format(table_name=table_name)                                                                                                              

    def __init__(self, _session):
        self._session = _session
        self.maybe_create_schema()
        self.insert_prep_stmt = _session.prepare(self.insert_stmt)
        self.select_all_feedbacks_for_hotel_id_prep_stmt = _session.prepare(self.select_all_feedbacks_for_hotel_id)
    
    def maybe_create_schema(self):
        self._session.execute(self.create_stmt)

    def create_feedback(self, feedback):
        def handle_success(results):
            print("feedback added")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)

        insert_future = self._session.execute_async(self.insert_prep_stmt.bind({
            'hotel_id':feedback.hotel_id,
            'customer_id':feedback.customer_id,
            'customer_name':feedback.customer_name,
            'feedback_comment':feedback.feedback_comment,
            'ratings':feedback.ratings,
            'time_of_feedback':feedback.time_of_feedback,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    def get_feedback_by_hotel_id(self,hotel_id):
        result = self._session.execute(self.select_all_feedbacks_for_hotel_id_prep_stmt.bind({
            'hotel_id': hotel_id}
        ))
        return result

    def get_feedback_exits(self,hotel_id):
        count = 0
        result = self._session.execute(self.select_all_feedbacks_for_hotel_id_prep_stmt.bind({
            'hotel_id': hotel_id}
        ))
        for row in result:
            count += 1
        if count >= 1:
            return True
        else:
            return False
    