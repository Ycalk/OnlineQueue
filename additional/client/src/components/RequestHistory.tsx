import { Timeline, Text } from '@mantine/core';
import { ApiRequest } from '../types/requests';
import dayjs from 'dayjs';

interface RequestHistoryProps {
    request: ApiRequest;
}

export function RequestHistory({ request }: RequestHistoryProps) {
    const events = [
        ...request.status_history.map(h => ({
            id: `status-${h.occurred_at}`,
            type: 'status',
            title: 'Изменение статуса',
            description: `Новый статус: ${h.status}`,
            time: h.occurred_at
        })),
        ...request.priority_history.map(h => ({
            id: `priority-${h.occurred_at}`,
            type: 'priority',
            title: 'Изменение приоритета',
            description: `Новый приоритет: ${h.priority}`,
            time: h.occurred_at
        })),
        ...request.confirmation_datetime_history.map(h => ({
            id: `confirm-${h.occurred_at}`,
            type: 'confirmation',
            title: 'Назначено время',
            description: `${h.confirmation_datetime.date} ${h.confirmation_datetime.time_start}-${h.confirmation_datetime.time_end}`,
            time: h.occurred_at
        })),
        ...request.comments.map(c => ({
            id: `comment-${c.created_at}`,
            type: 'comment',
            title: c.author === 'visiter' ? 'Ваш комментарий' : 'Комментарий владельца',
            description: c.text,
            time: c.created_at
        }))
    ];

    const sortedEvents = events.sort((a, b) => a.time - b.time);

    return (
        <Timeline active={sortedEvents.length} bulletSize={20} lineWidth={2}>
            {sortedEvents.map((item) => (
                <Timeline.Item key={item.id} title={<Text size="sm" fw={500}>{item.title}</Text>}>
                    <Text size="xs" mt={4}>{item.description}</Text>
                    <Text size="xs" c="dimmed" mt={4}>
                        {dayjs.unix(item.time).format('DD.MM.YYYY HH:mm')}
                    </Text>
                </Timeline.Item>
            ))}
        </Timeline>
    );
}
