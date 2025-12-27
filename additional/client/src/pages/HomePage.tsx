import { useMemo, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMediaQuery } from '@mantine/hooks';
import { LayoutGroup } from 'framer-motion';
import { api } from '../api/ApiClient';
import 'dayjs/locale/ru';
import '@mantine/dates/styles.css';
import { notifications } from '@mantine/notifications';

import { AppShell, Container, TextInput, Button, Group, Title, Divider, Stack, Loader, Center, Text, Skeleton } from '@mantine/core';
import { IconSearch, IconPlus, IconCheck, IconX } from '@tabler/icons-react';

import { Header } from '../components/Header';
import { QueueCard, QueueDisplay } from '../components/QueueCard';
import { CreateQueueModal, CreateQueuePayload } from '../components/CreateQueueModal';

interface ApiQueue {
    id: string;
    owner_id: string;
    name: string;
    description: string | null;
    cleanup_period_days: number;
    reception_time_start: string;
    reception_time_end: string;
    requests_avg_duration_seconds: number | null;
    is_active: boolean;
}

interface ApiUser {
    first_name: string;
    last_name: string;
    patronymic: string | null;
}

function HomePage() {
    const navigate = useNavigate();
    const isMobile = useMediaQuery('(max-width: 48em)');
    const isTablet = useMediaQuery('(max-width: 75em)');
    const columnsCount = isMobile ? 1 : isTablet ? 2 : 3;

    const [isCreating, setIsCreating] = useState(false);

    const [queues, setQueues] = useState<QueueDisplay[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [expandedQueueId, setExpandedQueueId] = useState<string | null>(null);
    const [search, setSearch] = useState('');
    const [showCreateQueue, setShowCreateQueue] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const queuesData = await api.request<ApiQueue[]>('/api/v1/queues');
                const uniqueOwnerIds = Array.from(new Set(queuesData.map(q => q.owner_id)));
                const usersMap = new Map<string, string>();

                await Promise.all(uniqueOwnerIds.map(async (userId) => {
                    try {
                        const u = await api.request<ApiUser>(`/api/v1/users/${userId}`);
                        const shortName = `${u.last_name} ${u.first_name[0]}.` + (u.patronymic ? `${u.patronymic[0]}.` : '');
                        usersMap.set(userId, shortName);
                    } catch (e) {
                        usersMap.set(userId, 'Неизвестный');
                    }
                }));

                const mergedData: QueueDisplay[] = queuesData.map(q => ({
                    ...q,
                    ownerName: usersMap.get(q.owner_id) || 'Неизвестный'
                }));
                setQueues(mergedData);
            } catch (err) {
                console.error(err);
                setError('Не удалось загрузить очереди');
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, []);

    const filteredQueues = useMemo(() => {
        const q = search.trim().toLowerCase();
        let result = queues;

        if (q) {
            result = queues.filter((x) =>
                `${x.name} ${x.ownerName} ${x.description ?? ''}`.toLowerCase().includes(q)
            );
        }
        const activeQueues = result.filter(queue => queue.is_active);
        const inactiveQueues = result.filter(queue => !queue.is_active);
        return [...activeQueues, ...inactiveQueues];
    }, [queues, search]);

    const columns = useMemo(() => {
        const cols: QueueDisplay[][] = Array.from({ length: columnsCount }, () => []);
        filteredQueues.forEach((queue, index) => {
            cols[index % columnsCount].push(queue);
        });
        return cols;
    }, [filteredQueues, columnsCount]);

    const handleCreateQueue = () => {
        if (!localStorage.getItem('access_token')) {
            navigate('/?action=login');
            return;
        }
        setShowCreateQueue(true);
    };

    const handleQueueSubmit = async (data: CreateQueuePayload) => {
        try {
            setIsCreating(true);

            const createdQueue = await api.request<ApiQueue>('/api/v1/queues', 'POST', data);

            notifications.show({
                title: 'Успех',
                message: 'Очередь успешно создана',
                color: 'green',
                icon: <IconCheck size={18} />,
            });

            setShowCreateQueue(false);
            window.location.reload();

        } catch (error: any) {
            console.error('Ошибка при создании:', error);
            notifications.show({
                title: 'Ошибка',
                message: error.message || 'Не удалось создать очередь',
                color: 'red',
            });
        } finally {
            setIsCreating(false);
        }
    };

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <Header />
            <AppShell.Main>
                <Container size="80%" py="md">
                    <Title order={1} mb="lg">Доступные очереди</Title>
                    <Group mb="lg" justify="space-between">
                        <Group>
                            <TextInput
                                placeholder="Поиск..."
                                style={{ width: 300 }}
                                value={search}
                                onChange={(e) => setSearch(e.currentTarget.value)}
                                leftSection={<IconSearch size={16} />}
                            />
                        </Group>
                        <Button leftSection={<IconPlus size={16} />} onClick={handleCreateQueue}>Создать очередь</Button>
                    </Group>
                    <Divider size={2} my="sm" />

                    {isLoading ? (
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                            {Array.from({ length: columnsCount }).map((_, colIndex) => (
                                <Stack key={colIndex} gap="md" style={{ flex: 1 }}>
                                    {Array.from({ length: 3 }).map((__, itemIndex) => (
                                        <div
                                            key={itemIndex}
                                            style={{
                                                border: '1px solid #dee2e6',
                                                borderRadius: '8px',
                                                padding: '16px',
                                                backgroundColor: 'white'
                                            }}
                                        >
                                            <Group justify="space-between" mb="xs">
                                                <Group>
                                                    <Skeleton height={38} width={38} radius="md" />
                                                    <Skeleton height={20} width={140} radius="xl" />
                                                </Group>
                                                <Skeleton height={20} width={60} radius="xl" />
                                            </Group>

                                            <Group mt="md" mb="xs">
                                                <Skeleton height={16} width={16} radius="xl" />
                                                <Skeleton height={12} width={100} radius="xl" />
                                            </Group>

                                            <Stack gap={6} mt="md">
                                                <Skeleton height={8} radius="xl" />
                                                <Skeleton height={8} radius="xl" />
                                                <Skeleton height={8} width="70%" radius="xl" />
                                            </Stack>

                                            <Skeleton height={36} radius="md" mt="lg" />
                                        </div>
                                    ))}
                                </Stack>
                            ))}
                        </div>
                    ) : error ? (
                        <Text c="red" ta="center">{error}</Text>
                    ) : (
                        <LayoutGroup>
                            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                                {columns.map((colItems, colIndex) => (
                                    <Stack key={colIndex} gap="md" style={{ flex: 1 }}>
                                        {colItems.map(queue => (
                                            <QueueCard
                                                key={queue.id}
                                                queue={queue}
                                                isOpen={expandedQueueId === queue.id}
                                                onToggle={() => setExpandedQueueId(expandedQueueId === queue.id ? null : queue.id)}
                                            />
                                        ))}
                                    </Stack>
                                ))}
                            </div>
                        </LayoutGroup>
                    )}

                    <CreateQueueModal
                        opened={showCreateQueue}
                        onClose={() => setShowCreateQueue(false)}
                        onSubmit={handleQueueSubmit}
                    />
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}

export default HomePage;
