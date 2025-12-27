import { useEffect, useState, useMemo } from 'react';
import {
    Container,
    Title,
    Text,
    Paper,
    Group,
    Stack,
    Badge,
    ActionIcon,
    Loader,
    Button,
    TextInput,
    NumberInput,
    Textarea,
    Switch,
    ThemeIcon,
    Collapse,
    Divider,
    Box,
    AppShell,
    Center,
    Skeleton
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import {
    IconX,
    IconActivity,
    IconChevronDown,
    IconChevronUp,
    IconSearch,
    IconPlus,
} from '@tabler/icons-react';
import { useMediaQuery } from '@mantine/hooks';
import { api } from '../api/ApiClient';
import { Header } from '../components/Header';
import { CreateQueueModal, CreateQueuePayload } from '../components/CreateQueueModal';

import { LayoutGroup, motion } from 'framer-motion';

interface Queue {
    id: string;
    name: string;
    description: string;
    cleanup_period_days: number;
    is_active: boolean;
    requests: any[];
}

interface ApiQueueResponse extends Queue {
    owner_id: string;
    reception_time_start: string;
    reception_time_end: string;
}

export default function QueueSettingsPage() {
    const [queues, setQueues] = useState<Queue[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const [search, setSearch] = useState('');
    const [showCreateQueue, setShowCreateQueue] = useState(false);
    const [isCreating, setIsCreating] = useState(false);

    const isMobile = useMediaQuery('(max-width: 48em)');
    const columnsCount = isMobile ? 1 : 2;

    const fetchQueues = async () => {
        try {
            const data = await api.request<Queue[]>('/api/v1/queues/my', 'GET');
            setQueues(data);
        } catch (e: any) {
            console.error(e);
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось загрузить очереди', color: 'red' });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchQueues();
    }, []);

    const filteredQueues = useMemo(() => {
        const q = search.trim().toLowerCase();
        let result = queues;

        if (q) {
            result = queues.filter((x) =>
                `${x.name} ${x.description ?? ''}`.toLowerCase().includes(q)
            );
        }

        const activeQueues = result.filter(queue => queue.is_active);
        const inactiveQueues = result.filter(queue => !queue.is_active);

        return [...activeQueues, ...inactiveQueues];
    }, [queues, search]);

    const columns = useMemo(() => {
        const cols: Queue[][] = Array.from({ length: columnsCount }, () => []);
        filteredQueues.forEach((queue, index) => {
            cols[index % columnsCount].push(queue);
        });
        return cols;
    }, [filteredQueues, columnsCount]);

    const totalQueues = queues.length;
    const activeQueuesCount = queues.filter(q => q.is_active).length;
    const totalRequests = queues.reduce((acc, q) => acc + (q.requests?.length || 0), 0);

    const handleQueueSubmit = async (data: CreateQueuePayload) => {
        try {
            setIsCreating(true);
            await api.request<ApiQueueResponse>('/api/v1/queues', 'POST', data);

            notifications.show({
                title: 'Успех',
                message: 'Очередь успешно создана',
                color: 'green',
            });

            setShowCreateQueue(false);
            fetchQueues();
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
                    <Title order={1} mb="lg">Управление очередями</Title>

                    {isLoading ? (
                        <Group mb="xs">
                            <Skeleton height={20} width={150} radius="sm" />
                            <Skeleton height={20} width={150} radius="sm" />
                            <Skeleton height={20} width={150} radius="sm" />
                        </Group>
                    ) : (
                        <Group mb="xs">
                            <Text size="sm">Всего очередей: <strong>{totalQueues}</strong></Text>
                            <Text size="sm">Активные очереди: <strong>{activeQueuesCount}</strong></Text>
                            <Text size="sm">Всего заявок: <strong>{totalRequests}</strong></Text>
                        </Group>
                    )}



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
                        <Button leftSection={<IconPlus size={16} />} onClick={() => setShowCreateQueue(true)}>
                            Создать очередь
                        </Button>
                    </Group>

                    <Divider size={2} my="sm" />
                    {isLoading ? (
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                            {Array.from({ length: columnsCount }).map((_, colIndex) => (
                                <Stack key={colIndex} gap="lg" style={{ flex: 1 }}>
                                    {Array.from({ length: 3 }).map((_, cardIndex) => (
                                        <Paper key={cardIndex} withBorder radius="md" shadow="sm" p="md">
                                            <Group justify="space-between">
                                                <Group>
                                                    <Skeleton height={32} width={32} radius="sm" /> 
                                                    <Skeleton height={20} width={150} radius="sm" />
                                                </Group>
                                                <Group>
                                                    <Skeleton height={20} width={80} radius="xl" />
                                                    <Skeleton height={28} width={28} radius="sm" />
                                                </Group>
                                            </Group>
                                        </Paper>
                                    ))}
                                </Stack>
                            ))}
                        </div>
                    ) : (
                        filteredQueues.length === 0 ? (
                            <Text c="dimmed" ta="center" mt="xl">
                                {search ? 'Ничего не найдено по вашему запросу.' : 'У вас пока нет созданных очередей.'}
                            </Text>
                        ) : (
                            <LayoutGroup>
                                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                                    {columns.map((colItems, colIndex) => (
                                        <Stack key={colIndex} gap="lg" style={{ flex: 1 }}>
                                            {colItems.map(queue => (
                                                <QueueEditCard
                                                    key={queue.id}
                                                    queue={queue}
                                                    onUpdate={fetchQueues}
                                                />
                                            ))}
                                        </Stack>
                                    ))}
                                </div>
                            </LayoutGroup>
                        )
                    )}

                    <CreateQueueModal
                        opened={showCreateQueue}
                        onClose={() => setShowCreateQueue(false)}
                        onSubmit={handleQueueSubmit}
                        isLoading={isCreating}
                    />
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}

function QueueEditCard({ queue, onUpdate }: { queue: Queue, onUpdate: () => void }) {
    const [opened, setOpened] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm({
        initialValues: {
            name: queue.name,
            description: queue.description,
            cleanup_period_days: queue.cleanup_period_days,
        },
        validate: {
            name: (val) => (val.trim().length < 3 ? 'Название слишком короткое' : null),
            cleanup_period_days: (val) => (val < 0 ? 'Не может быть отрицательным' : null),
        }
    });

    const handleToggleActive = async () => {
        setIsSubmitting(true);
        try {
            await api.request(`/api/v1/queues/${queue.id}/toggle`, 'POST');
            notifications.show({ title: 'Успех', message: `Очередь ${!queue.is_active ? 'активирована' : 'остановлена'}`, color: 'green' });
            onUpdate();
        } catch (e) {
            notifications.show({ title: 'Ошибка', message: 'Не удалось изменить статус', color: 'red' });
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleSave = async (values: typeof form.values) => {
        setIsSubmitting(true);
        try {
            const promises = [];
            if (values.name !== queue.name) {
                promises.push(api.request(`/api/v1/queues/${queue.id}/name`, 'PATCH', { new_name: values.name }));
            }
            if (values.description !== queue.description) {
                promises.push(api.request(`/api/v1/queues/${queue.id}/description`, 'PATCH', { new_description: values.description }));
            }
            if (values.cleanup_period_days !== queue.cleanup_period_days) {
                promises.push(api.request(`/api/v1/queues/${queue.id}/cleanup-period`, 'PATCH', { new_cleanup_period_days: values.cleanup_period_days }));
            }

            if (promises.length > 0) {
                await Promise.all(promises);
                notifications.show({ title: 'Сохранено', message: 'Настройки очереди обновлены', color: 'green' });
                onUpdate();
                form.resetDirty();
            }
        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Ошибка', message: 'Не удалось сохранить изменения', color: 'red' });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <motion.div layout
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ layout: { type: "spring", stiffness: 300, damping: 30 } }}>
            <Paper withBorder radius="md" shadow="sm">
                <Group justify="space-between" p="md" onClick={() => setOpened(!opened)} style={{ cursor: 'pointer' }}>
                    <Group>
                        <ThemeIcon color={queue.is_active ? 'custom-pink' : 'gray'} variant="light" size="lg">
                            {queue.is_active ? <IconActivity size={20} /> : <IconX size={20} />}
                        </ThemeIcon>
                        <div>
                            <Text fw={600}>{queue.name}</Text>
                        </div>
                    </Group>

                    <Group>
                        <Badge color={queue.is_active ? '#5FBF24' : '#FA5252'} variant="dot">
                            {queue.is_active ? 'Активна' : 'Неактивна'}
                        </Badge>
                        <ActionIcon variant="subtle" color="gray">
                            {opened ? <IconChevronUp /> : <IconChevronDown />}
                        </ActionIcon>
                    </Group>
                </Group>

                <Collapse in={opened}>
                    <Divider />
                    <Box p="md">
                        <Group mb="md" gap="xs">
                            <Badge variant="outline" color="custom-pink">Заявок: {queue.requests?.length || 0}</Badge>
                        </Group>

                        <form onSubmit={form.onSubmit(handleSave)}>
                            <Stack gap="md">
                                <TextInput
                                    label="Название очереди"
                                    placeholder="Введите название очереди"
                                    {...form.getInputProps('name')}
                                />
                                <Textarea
                                    label="Описание"
                                    placeholder="Введите описание очереди"
                                    autosize
                                    minRows={2}
                                    style={{ gridColumn: 'span 1 / span 2' }}
                                    {...form.getInputProps('description')}
                                />

                                <NumberInput
                                    label="Период автоочистки (дней)"
                                    min={0}
                                    {...form.getInputProps('cleanup_period_days')}
                                />
                                <Text size="xs" c="dimmed" mt={-5}>Через указанное количество дней запрос попадет в архив.</Text>

                            </Stack>

                            <Group justify="space-between" mt="xl">
                                <Switch
                                    label={queue.is_active ? "Деактивировать очередь" : "Активировать очередь"}
                                    checked={queue.is_active}
                                    onChange={handleToggleActive}
                                    color="custom-pink"
                                    size="md"
                                    disabled={isSubmitting}
                                />

                                <Button
                                    type="submit"
                                    disabled={!form.isDirty() || isSubmitting}
                                    loading={isSubmitting}
                                >
                                    Сохранить изменения
                                </Button>
                            </Group>
                        </form>
                    </Box>
                </Collapse>
            </Paper>
        </motion.div>
    );
}
