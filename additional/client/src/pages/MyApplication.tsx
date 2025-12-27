import { useEffect, useState, useMemo } from 'react';
import {
    AppShell,
    Container,
    TextInput,
    Group,
    Title,
    SimpleGrid,
    SegmentedControl,
    Divider,
    Text,
    Paper,
    Stack,
    Skeleton,
    Box
} from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { notifications } from '@mantine/notifications';

import { Header } from '../components/Header';
import { ApplicationCard } from '../components/ApplicationCard';
import { api } from '../api/ApiClient';
import { ApiRequest, ApiQueue, ApiUser, EnrichedRequest } from '../types/requests';

type FilterStatus = 'waiting' | 'accepted' | 'archived';

export default function MyApplication() {
    const [requests, setRequests] = useState<ApiRequest[]>([]);
    const [queuesMap, setQueuesMap] = useState<Record<string, ApiQueue>>({});
    const [usersMap, setUsersMap] = useState<Record<string, ApiUser>>({});

    const [isLoading, setIsLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [activeTab, setActiveTab] = useState<FilterStatus>('waiting');

    const fetchRequests = async () => {
        try {
            const data = await api.request<ApiRequest[]>('/api/v1/requests/my', 'GET');
            setRequests(data);
            const queueIds = Array.from(new Set(data.map(r => r.queue_id)));
            const loadedQueues: Record<string, ApiQueue> = {};
            const queuePromises = queueIds.map(async (qId) => {
                if (queuesMap[qId]) {
                    loadedQueues[qId] = queuesMap[qId];
                    return;
                }
                try {
                    const q = await api.request<ApiQueue>(`/api/v1/queues/${qId}`, 'GET');
                    loadedQueues[qId] = q;
                } catch (e) {
                    console.error(`Failed to load queue ${qId}`, e);
                }
            });
            await Promise.all(queuePromises);
            setQueuesMap(prev => ({ ...prev, ...loadedQueues }));
            const ownerIds = Array.from(new Set(Object.values(loadedQueues).map(q => q.owner_id)));
            const loadedUsers: Record<string, ApiUser> = {};
            const userPromises = ownerIds.map(async (uId) => {
                if (usersMap[uId]) {
                    loadedUsers[uId] = usersMap[uId];
                    return;
                }
                try {
                    const u = await api.request<ApiUser>(`/api/v1/users/${uId}`, 'GET');
                    loadedUsers[uId] = u;
                } catch (e) {
                    console.error(`Failed to load user ${uId}`, e);
                }
            });
            await Promise.all(userPromises);
            setUsersMap(prev => ({ ...prev, ...loadedUsers }));
        } catch (e: any) {
            console.error(e);
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось загрузить заявки', color: 'red' });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        setIsLoading(true);
        fetchRequests();
    }, []);

    const filteredRequests = useMemo(() => {
        return requests.filter(req => {
            if (search) {
                const searchLower = search.toLowerCase();

                const purpose = req.purpose?.toLowerCase() || '';

                const queueData = queuesMap[req.queue_id];
                const queueName = queueData?.name?.toLowerCase() || '';
                const queueDesc = queueData?.description?.toLowerCase() || '';

                const ownerId = queueData?.owner_id;
                const ownerData = ownerId ? usersMap[ownerId] : undefined;

                const ownerFirstName = ownerData?.first_name?.toLowerCase() || '';
                const ownerLastName = ownerData?.last_name?.toLowerCase() || '';
                const ownerPatronymic = ownerData?.patronymic?.toLowerCase() || '';

                const ownerFullName = `${ownerLastName} ${ownerFirstName} ${ownerPatronymic}`.trim();
                const matchesSearch =
                    purpose.includes(searchLower) ||
                    queueName.includes(searchLower) ||
                    queueDesc.includes(searchLower) ||
                    ownerFullName.includes(searchLower);

                if (!matchesSearch) {
                    return false;
                }
            }
            if (activeTab === 'archived') {
                return req.is_archived;
            }
            if (activeTab === 'waiting') {
                return req.status === 'pending' && !req.is_archived;
            }
            if (activeTab === 'accepted') {
                return req.status === 'accepted' && !req.is_archived;
            }

            return false;
        });
    }, [requests, search, activeTab, queuesMap, usersMap]);

    const stats = useMemo(() => {
        return {
            total: requests.length,
            active: requests.filter(r => !r.is_archived && (r.status === 'pending' || r.status === 'accepted')).length
        };
    }, [requests]);

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <Header />

            <AppShell.Main>
                <Container size="80%" py="md">
                    <Title order={1} mb="lg">Мои заявки</Title>

                    {isLoading ? (
                        <Group mb="xs">
                            <Skeleton height={20} width={120} radius="sm" />
                            <Skeleton height={20} width={120} radius="sm" />
                        </Group>
                    ) : (
                        <Group mb="xs">
                            <Text size="sm">Всего заявок: <strong>{stats.total}</strong></Text>
                            <Text size="sm">Активных заявок: <strong>{stats.active}</strong></Text>
                        </Group>
                    )}


                    <Group mb="lg" justify="space-between">
                        <TextInput
                            placeholder="Поиск..."
                            style={{ width: 300 }}
                            value={search}
                            onChange={(e) => setSearch(e.currentTarget.value)}
                            leftSection={<IconSearch size={16} />}
                        />

                        <SegmentedControl
                            value={activeTab}
                            onChange={(val) => setActiveTab(val as FilterStatus)}
                            data={[
                                { label: 'Ожидание', value: 'waiting' },
                                { label: 'Принято', value: 'accepted' },
                                { label: 'Архив', value: 'archived' },
                            ]}
                        />
                    </Group>

                    <Divider size={2} my="sm" />

                    {isLoading ? (
                        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
                            {Array.from({ length: 6 }).map((_, index) => (
                                <Paper
                                    key={index}
                                    withBorder
                                    p="lg"
                                    radius="md"
                                    shadow="sm"
                                    h={500}
                                    style={{ display: 'flex', flexDirection: 'column' }}
                                >
                                    <Group justify="space-between" mb="xs">
                                        <Skeleton height={28} width="70%" radius="sm" />
                                    </Group>

                                    <Group gap="xs" mb="sm">
                                        <Skeleton height={20} width={20} radius="xl" />
                                        <Skeleton height={16} width="40%" radius="sm" />
                                    </Group>

                                    <Group justify="space-between" mb="sm">
                                        <Skeleton height={20} width={80} radius="xl" />
                                        <Skeleton height={24} width={120} radius="sm" />
                                    </Group>

                                    <Divider mb="sm" />

                                    <Box style={{ flex: 1 }}>
                                        <Stack gap="md">
                                            <Skeleton height={20} width="30%" radius="sm" />
                                            <Skeleton height={60} radius="sm" />

                                            <Skeleton height={20} width="25%" radius="sm" />
                                            <Skeleton height={20} width="80%" radius="sm" />

                                            <Skeleton height={20} width="35%" radius="sm" />
                                            <Skeleton height={40} radius="sm" />
                                        </Stack>
                                    </Box>

                                    <Divider my="sm" />

                                    <Group justify="end">
                                        <Skeleton height={30} width={100} radius="sm" />
                                    </Group>
                                </Paper>
                            ))}
                        </SimpleGrid>
                    ) : filteredRequests.length === 0 ? (
                        <Text c="dimmed" ta="center" mt="xl">Заявок не найдено</Text>
                    ) : (
                        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
                            {filteredRequests.map((req) => (
                                <ApplicationCard
                                    key={req.id}
                                    request={{
                                        ...req,
                                        queueData: queuesMap[req.queue_id],
                                        ownerData: queuesMap[req.queue_id] ? usersMap[queuesMap[req.queue_id].owner_id] : undefined
                                    }}
                                    onUpdate={fetchRequests}
                                />
                            ))}
                        </SimpleGrid>
                    )}
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}
