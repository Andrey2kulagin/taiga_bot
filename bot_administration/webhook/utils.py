def parse_taiga_webhook(data):
    action = data['action']
    issue_data = data['data']
    issue_subject = issue_data['subject']
    issue_permalink = issue_data['permalink']

    if action == 'create':
        return f'Создан новый issue: "{issue_subject}" ({issue_permalink})'
    elif action == 'change':
        change_data = data['change']
        notification = f'Изменен issue: "{issue_subject}" ({issue_permalink}). Изменения:'

        if 'type' in change_data['diff']:
            type_change = change_data['diff']['type']
            notification += f'\n- Тип изменен с "{type_change["from"]}" на "{type_change["to"]}"'

        if 'status' in change_data['diff']:
            status_change = change_data['diff']['status']
            notification += f'\n- Статус изменен с "{status_change["from"]}" на "{status_change["to"]}"'

        if 'severity' in change_data['diff']:
            severity_change = change_data['diff']['severity']
            notification += f'\n- Важность изменена с "{severity_change["from"]}" на "{severity_change["to"]}"'

        if 'priority' in change_data['diff']:
            priority_change = change_data['diff']['priority']
            notification += f'\n- Приоритет изменен с "{priority_change["from"]}" на "{priority_change["to"]}"'

        if 'assigned_to' in change_data['diff']:
            assigned_to_change = change_data['diff']['assigned_to']
            from_assigned = assigned_to_change['from'] if assigned_to_change['from'] else 'никто'
            to_assigned = assigned_to_change['to'] if assigned_to_change['to'] else 'никто'
            notification += f'\n- Изменен ответственный с "{from_assigned}" на "{to_assigned}"'

        if 'due_date' in change_data['diff']:
            due_date_change = change_data['diff']['due_date']
            notification += f'\n- Срок выполнения изменен с "{due_date_change["from"]}" на "{due_date_change["to"]}"'

        if 'is_blocked' in change_data['diff']:
            is_blocked_change = change_data['diff']['is_blocked']
            notification += f'\n- Изменено значение "is_blocked" с "{is_blocked_change["from"]}" на "{is_blocked_change["to"]}"'

        return notification
    elif action == 'delete':
        return f'Удален issue: "{issue_subject}" ({issue_permalink})'
    else:
        return 'Действие не поддерживается'
