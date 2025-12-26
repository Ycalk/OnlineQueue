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
    SimpleGrid,
    ThemeIcon,
    Collapse,
    Divider,
    Box,
    AppShell
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import {
    IconX,
    IconList,
    IconActivity,
    IconClock,
    IconChevronDown,
    IconChevronUp
} from '@tabler/icons-react';
import { useMediaQuery } from '@mantine/hooks';
import { api } from '../api/ApiClient';
import { Header } from '../components/Header';


interface Queue {
    id: string;
    name: string;
    description: string;
    cleanup_period_days: number;
    is_active: boolean;
    requests: any[];
}

export default function QueueSettingsPage() {
    const [queues, setQueues] = useState<Queue[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const isMobile = useMediaQuery('(max-width: 48em)');
    const columnsCount = isMobile ? 1 : 2;

    const columns = useMemo(() => {
        const cols: Queue[][] = Array.from({ length: columnsCount }, () => []);
        queues.forEach((queue, index) => {
            cols[index % columnsCount].push(queue);
        });
        return cols;
    }, [queues, columnsCount]);

    const fetchQueues = async () => {
        try {
            const data = await api.request<Queue[]>('/api/v1/queues/my', 'GET');
            setQueues(data);
        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Ошибка', message: 'Не удалось загрузить очереди', color: 'red' });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchQueues();
    }, []);

    const totalQueues = queues.length;
    const activeQueues = queues.filter(q => q.is_active).length;
    const totalRequests = queues.reduce((acc, q) => acc + (q.requests?.length || 0), 0);

    if (isLoading) {
        return (
            <Container size="lg" py="xl">
                <Group justify="center"><Loader /></Group>
            </Container>
        );
    }

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <Header />
            <AppShell.Main>
                <Container size="80%" py="md">
                    <Title order={1} mb="lg">Управление очередями</Title>

                    {/* Блок статистики */}
                    <SimpleGrid cols={{ base: 1, sm: 3 }} mb="xl">
                        <StatCard title="Всего очередей" value={totalQueues} icon={<IconList size={24} />} color="blue" />
                        <StatCard title="Активные очереди" value={activeQueues} icon={<IconActivity size={24} />} color="custom-pink" />
                        <StatCard title="Всего заявок" value={totalRequests} icon={<IconClock size={24} />} color="grape" />
                    </SimpleGrid>

                    <Divider size={2} my="sm" />

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
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}

function StatCard({ title, value, icon, color }: { title: string, value: number, icon: React.ReactNode, color: string }) {
    return (
        <Paper withBorder p="md" radius="md">
            <Group justify="space-between">
                <div>
                    <Text size="xs" c="dimmed" fw={700} tt="uppercase">
                        {title}
                    </Text>
                    <Text fw={700} size="xl">
                        {value}
                    </Text>
                </div>
                <ThemeIcon color={color} variant="light" size={38} radius="md">
                    {icon}
                </ThemeIcon>
            </Group>
        </Paper>
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
    );
}
