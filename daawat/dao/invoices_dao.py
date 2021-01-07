from daawat.util.cql_file_util import get_cql_schema_string_from_file
from daawat.util.data_type_util import uuid_from_string
from daawat.model.inovice import Invoices

class InvoicesDAO(object):

    table_name = "invoices"

    create_stmt = get_cql_schema_string_from_file(table_name)

    insert_stmt = 'INSERT INTO {table_name} (hotel_id,customer_id,order_id,invoice_id,product,time_of_invoice,price,quantity,grand_total) ' \
                  'VALUES (:hotel_id,:customer_id,:order_id,:invoice_id,:product,:time_of_invoice,:price,:quantity,:grand_total);'.format(table_name=table_name)

    select_all_invoices_for_invoice_id = 'SELECT * FROM {table_name} WHERE invoice_id = :invoice_id ALLOW FILTERING;'.format(table_name=table_name)

    select_all_invoices_for_customer_id = 'SELECT * FROM {table_name} WHERE customer_id = :customer_id LIMIT 1 ALLOW FILTERING;'.format(table_name=table_name)

    update_status = 'UPDATE {table_name} SET status = :status WHERE hotel_id = :hotel_id AND customer_id = :customer_id AND order_id = :order_id AND time_of_order = :time_of_order' \
                                              ''.format(table_name=table_name)                                                                                                                               

    def __init__(self, _session):
        self._session = _session
        self.maybe_create_schema()
        self.insert_prep_stmt = _session.prepare(self.insert_stmt)
        self.select_all_invoices_for_invoice_id_prep_stmt = _session.prepare(self.select_all_invoices_for_invoice_id)
        self.select_all_invoices_for_customer_id_prep_stmt = _session.prepare(self.select_all_invoices_for_customer_id)
    
    def maybe_create_schema(self):
        self._session.execute(self.create_stmt)

    def create_invoice(self, invoice):
        def handle_success(results):
            print("invoice added")

        def handle_error(exception):
            raise Exception('Failed to write row: ' + exception)

        insert_future = self._session.execute_async(self.insert_prep_stmt.bind({
            'hotel_id':invoice.hotel_id,
            'customer_id':invoice.customer_id,
            'order_id':invoice.order_id,
            'invoice_id':invoice.invoice_id,
            'product':invoice.product_id,
            'time_of_invoice':invoice.time_of_invoice,
            'price':invoice.price,
            'quantity':invoice.quantity,
            'grand_total':invoice.grand_total,
        }))

        insert_future.add_callbacks(handle_success, handle_error)

    def get_invoice_by_invoice_id(self,invoice_id):
        result = self._session.execute(self.select_all_invoices_for_invoice_id_prep_stmt.bind({
            'invoice_id': invoice_id}
        ))
        return result
    
    def get_invoice_by_customer_id(self,customer_id):
        invoices = []

        if len(customer_id) == 1:
            result = self._session.execute(self.select_all_invoices_for_customer_id_prep_stmt.bind({
                'customer_id':customer_id[0]}
            ))

            return result
        
        for customer in customer_id:
            result = self._session.execute(self.select_all_invoices_for_customer_id_prep_stmt.bind({
                'customer_id':customer}
            ))
            for out in result:
                invoices.append(out)
        return invoices