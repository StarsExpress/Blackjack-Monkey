from data_access import DataAccess
import uuid

data_access = DataAccess()

class DataPersistence(object):
    """An object for login, creation and update from user."""
    def __init__(self, user_object):
        self.user = user_object

        # Track existing user names.
        data_access.select('Select user_name From user_info', tuple = None)
        self.existing_user_names = [d[0] for d in data_access.fetchall()]

    def find(self): # Check if a user name already exists.
        if self.user.name in self.existing_user_names:
            return ''.join(['User name ', self.user.name, ' found.'])

        else:
            return ''.join(['User name ', self.user.name, ' not found.'])

    def login(self): # Login for an input user name.
        self.login_summary = {}
        if self.user.name == '': # If the input user name is empty.
            self.login_summary['Topic'] = 'Your user name is empty. Please try again.'
            self.login_summary['Description'] = ''

        else:
            if self.user.name in self.existing_user_names: # If a user name has already been created before.
                update_time = self.user.submit_time
                update_year, update_month, update_day = update_time.strftime('%Y'), update_time.strftime(
                    '%B'), update_time.strftime('%d').lstrip('0')
                update_hour, update_minute, update_second = update_time.strftime('%H'), update_time.strftime(
                    '%M'), str(update_time.second + round(update_time.microsecond / 1000000, 0)).replace('.0', '')
                update_second = '0' + update_second if int(update_second) < 10 else update_second

                update_day_mod = int(update_day) % 10
                if (update_day_mod >= 1) & (update_day_mod <= 3):
                    if (update_day_mod >= 20) | (update_day_mod < 10):
                        update_day = update_day + 'st' if update_day_mod == 1 else (
                            update_day + 'nd' if update_day_mod == 2 else update_day + 'rd')
                    else:
                        update_day = update_day + 'th'
                else:
                    update_day = update_day + 'th'

                # Update latest update time.
                data_access.update("""Update user_info Set update_time = %s Where user_name = %s""",
                                          (update_time, self.user.name))
                data_access.commit()

                self.login_summary['Topic'] = ''.join([self.user.name, ' has been successfully updated.'])
                self.login_summary['Description'] = ''.join(
                    ['Updated at: ', update_year, ' ', update_month, ' ', update_day, ' ', update_hour, ':',
                     update_minute, ':', update_second, '.'])

            else: # If a user name is new, assign a user ID to it by uuid1 to prevent duplicates.
                create_time = self.user.submit_time
                create_year, create_month, create_day = create_time.strftime('%Y'), create_time.strftime(
                    '%B'), create_time.strftime('%d').lstrip('0')
                create_hour, create_minute, create_second = create_time.strftime('%H'), create_time.strftime(
                    '%M'), str(create_time.second + round(create_time.microsecond / 1000000, 0)).replace('.0', '')
                create_second = '0' + create_second if int(create_second) < 10 else create_second

                create_day_mod = int(create_day) % 10
                if (create_day_mod >= 1) & (create_day_mod <= 3):
                    if (create_day_mod >= 20) | (create_day_mod < 10):
                        create_day = create_day + 'st' if create_day_mod == 1 else (
                            create_day + 'nd' if create_day_mod == 2 else create_day + 'rd')
                    else:
                        create_day = create_day + 'th'
                else:
                    create_day = create_day + 'th'

                # Save user information into corresponding database and table.
                data_access.insert(
                    'Insert Into user_info (user_id, user_name, create_time, update_time) Values (%s, %s, %s, %s)',
                    (str(uuid.uuid1()), self.user.name, create_time, create_time))
                data_access.commit()
                # Update existing user names after the newest creation.
                data_access.select('Select user_name From user_info')
                self.existing_user_names = [d[0] for d in data_access.fetchall()]

                self.login_summary['Topic'] = ''.join([self.user.name, ' has been successfully created.'])
                self.login_summary['Description'] = ''.join(
                    ['Created at: ', create_year, ' ', create_month, ' ', create_day, ' ', create_hour, ':',
                     create_minute, ':', create_second, '.'])

        return self.login_summary

    def delete_account(self): # Delete selected user name.
        data_access.select("""Select user_id From user_info Where user_name = %s""",
        tuple = [(self.user.name)])
        user_id = [d[0] for d in data_access.fetchall()][0]

        data_access.delete("""Delete From user_info Where user_id = %s""",
                           [(user_id)])
        data_access.commit()

        return ''.join([self.user.name, ' has been successfully deleted.'])

# Run only if the name is __main__.
if __name__ == '__main__':
    main()