import React, { useEffect, useState, useMemo, useRef } from 'react';
import {
    AppShell,
    SegmentedControl,
    Card,
    Button,
    Textarea,
    NumberInput,
    Title,
    Text,
    Divider,
    Group,
    Stack,
    Container,
    Collapse,
    Timeline,
    ActionIcon,
    Paper,
    Box,
    ScrollArea,
    ThemeIcon,
    Center,
    SimpleGrid,
    Loader,
    Badge,
    MultiSelect,
    Popover,
    Skeleton
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
    IconChevronDown,
    IconUserOff,
    IconActivity,
    IconX,
    IconCalendarTime,
    IconCalendar,
    IconFilter
} from '@tabler/icons-react';
import dayjs from 'dayjs';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';
import '@mantine/dates/styles.css';
import { DateInput, TimeInput } from '@mantine/dates';
import { IconClock } from '@tabler/icons-react';
import { motion, AnimatePresence } from 'framer-motion';

import { RequestHistory } from '../components/RequestHistory';
import { Header } from '../components/Header';
import { api } from '../api/ApiClient';
import { ApiRequest, ApiQueue, ApiUser, EnrichedRequest, RequestPriority } from '../types/requests';

dayjs.extend(isSameOrBefore);

export const MyQueue: React.FC = () => {
    const [requests, setRequests] = useState<ApiRequest[]>([]);
    const [queuesMap, setQueuesMap] = useState<Record<string, ApiQueue>>({});
    const [usersMap, setUsersMap] = useState<Record<string, ApiUser>>({});
    const [isLoading, setIsLoading] = useState(true);

    const [selectedRequestId, setSelectedRequestId] = useState<string | null>(null);
    const [expandedInQueue, setExpandedInQueue] = useState(true);
    const [expandedWaiting, setExpandedWaiting] = useState(true);

    const [selectedQueueFilter, setSelectedQueueFilter] = useState<string[]>([]);

    const [scheduleDate, setScheduledDate] = useState<Date | null>(new Date());
    const [scheduleTime, setScheduleTime] = useState<string>('');
    const [scheduleDuration, setScheduleDuration] = useState<number>(15);
    const [comment, setComment] = useState('');
    const [isSubmittingTime, setIsSubmittingTime] = useState(false);
    const [isSubmittingComment, setIsSubmittingComment] = useState(false);

    const timeInputRef = useRef<HTMLInputElement>(null);

    const fetchData = async () => {
        try {
            const data = await api.request<ApiRequest[]>('/api/v1/requests/queue/my', 'GET');

            const activeRequests = data.filter(r => !r.is_archived && r.status !== 'rejected');
            setRequests(activeRequests);

            const queueIds = Array.from(new Set(activeRequests.map(r => r.queue_id)));
            const userIds = Array.from(new Set(activeRequests.map(r => r.user_id)));

            const loadedQueues: Record<string, ApiQueue> = { ...queuesMap };
            await Promise.all(queueIds.map(async (id) => {
                if (!loadedQueues[id]) {
                    try {
                        const q = await api.request<ApiQueue>(`/api/v1/queues/${id}`, 'GET');
                        loadedQueues[id] = q;
                    } catch (e) { console.error(e); }
                }
            }));
            setQueuesMap(loadedQueues);

            const loadedUsers: Record<string, ApiUser> = { ...usersMap };
            await Promise.all(userIds.map(async (id) => {
                if (!loadedUsers[id]) {
                    try {
                        const u = await api.request<ApiUser>(`/api/v1/users/${id}`, 'GET');
                        loadedUsers[id] = u;
                    } catch (e) { console.error(e); }
                }
            }));
            setUsersMap(loadedUsers);

        } catch (e: any) {
            console.error(e);
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось загрузить данные', color: 'red' });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        if (selectedRequestId) {
            const req = requests.find(r => r.id === selectedRequestId);
            if (req) {
                const dt = req.confirmed_datetime || req.preferred_datetime;
                const parsedDate = dayjs(dt.date).toDate();
                setScheduledDate(parsedDate);
                setScheduleTime(dt.time_start);
                setScheduleDuration(15);
                setComment('');
            }
        }
    }, [selectedRequestId, requests]);

    const queueOptions = useMemo(() => {
        return Object.values(queuesMap).map(q => ({
            value: q.id,
            label: q.name
        }));
    }, [queuesMap]);

    const { waitingList, inQueueList } = useMemo(() => {
        const waiting: EnrichedRequest[] = [];
        const inQueue: EnrichedRequest[] = [];

        requests.forEach(req => {
            if (selectedQueueFilter.length > 0 && !selectedQueueFilter.includes(req.queue_id)) {
                return;
            }

            const enriched: EnrichedRequest = {
                ...req,
                queueData: queuesMap[req.queue_id],
                ownerData: usersMap[req.user_id]
            };

            if (req.status === 'pending') {
                waiting.push(enriched);
            } else if (req.status === 'accepted') {
                inQueue.push(enriched);
            }
        });

        inQueue.sort((a, b) => {
            if (!a.confirmed_datetime || !b.confirmed_datetime) return 0;

            const now = dayjs();
            const endA = dayjs(`${a.confirmed_datetime.date} ${a.confirmed_datetime.time_end}`);
            const endB = dayjs(`${b.confirmed_datetime.date} ${b.confirmed_datetime.time_end}`);

            const isAPassed = endA.isBefore(now);
            const isBPassed = endB.isBefore(now);

            if (isAPassed && !isBPassed) return 1;
            if (!isAPassed && isBPassed) return -1;

            return a.confirmed_datetime.start_unix - b.confirmed_datetime.start_unix;
        });

        return { waitingList: waiting, inQueueList: inQueue };
    }, [requests, queuesMap, usersMap, selectedQueueFilter]);

    const selectedRequest = useMemo(() => {
        if (!selectedRequestId) return null;
        const req = requests.find(r => r.id === selectedRequestId);
        if (!req) return null;
        return {
            ...req,
            queueData: queuesMap[req.queue_id],
            ownerData: usersMap[req.user_id]
        } as EnrichedRequest;
    }, [selectedRequestId, requests, queuesMap, usersMap]);

    const formatDate = (date: Date | null): string => {
        if (!date || !(date instanceof Date)) {
            if (typeof date === 'string') {
                const d = new Date(date);
                if (!isNaN(d.getTime())) {
                    return d.toISOString().split('T')[0];
                }
            }
            return '';
        }

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const handleUpdateTime = async () => {
        if (!selectedRequestId) return;
        setIsSubmittingTime(true);
        try {
            await api.request(`/api/v1/requests/${selectedRequestId}/time`, 'PATCH', {
                date: formatDate(scheduleDate),
                time_start: scheduleTime,
                duration_minutes: scheduleDuration
            });
            notifications.show({ title: 'Успех', message: 'Время визита обновлено', color: 'green' });
            fetchData();
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось обновить время', color: 'red' });
        } finally {
            setIsSubmittingTime(false);
        }
    };

    const handleChangePriority = async (val: string) => {
        if (!selectedRequestId) return;
        const mappedPriority = val === 'Низкий' ? 'low' : val === 'Средний' ? 'medium' : 'high';

        const oldRequests = [...requests];
        setRequests(prev => prev.map(r => r.id === selectedRequestId ? { ...r, priority: mappedPriority as RequestPriority } : r));

        try {
            await api.request(`/api/v1/requests/${selectedRequestId}/priority`, 'PATCH', {
                new_priority: mappedPriority
            });
            notifications.show({ title: 'Успех', message: 'Приоритет изменен', color: 'green' });
        } catch (e: any) {
            setRequests(oldRequests);
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось изменить приоритет', color: 'red' });
        }
    };

    const handleReject = async () => {
        if (!selectedRequestId || !window.confirm('Вы действительно хотите отклонить эту заявку?')) return;
        try {
            await api.request(`/api/v1/requests/${selectedRequestId}/reject`, 'PATCH');
            notifications.show({ title: 'Отклонено', message: 'Заявка отклонена и перенесена в архив', color: 'blue' });
            setSelectedRequestId(null);
            fetchData();
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось отклонить заявку', color: 'red' });
        }
    };

    const handleSendComment = async () => {
        if (!selectedRequestId || !comment.trim()) return;
        setIsSubmittingComment(true);
        try {
            await api.request(`/api/v1/requests/${selectedRequestId}/comment`, 'POST', { text: comment });
            setComment('');
            notifications.show({ title: 'Успех', message: 'Комментарий добавлен', color: 'green' });
            fetchData();
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось отправить комментарий', color: 'red' });
        } finally {
            setIsSubmittingComment(false);
        }
    };

    const QueueCard: React.FC<{ item: EnrichedRequest; isSelected?: boolean; isPassed?: boolean }> = ({ item, isSelected = false, isPassed = false }) => {
        const userName = item.ownerData
            ? `${item.ownerData.last_name} ${item.ownerData.first_name}`
            : 'Загрузка...';

        const timeString = item.status === 'accepted' && item.confirmed_datetime
            ? `${item.confirmed_datetime.date} ${item.confirmed_datetime.time_start} - ${item.confirmed_datetime.time_end}`
            : `${item.preferred_datetime.date} ${item.preferred_datetime.time_start} - ${item.preferred_datetime.time_end} (Предпочтительно)`;

        const queueName = item.queueData ? item.queueData.name : 'Загрузка...';

        return (
            <Card
                p="sm"
                radius="md"
                withBorder
                style={{
                    cursor: 'pointer',
                    backgroundColor: isSelected ? '#fce7f3' : 'white',
                    borderColor: isSelected ? '#ec4899' : '#e5e7eb',
                    borderWidth: 2,
                    opacity: isPassed ? 0.6 : 1
                }}
                onClick={() => setSelectedRequestId(item.id)}
            >
                <Stack gap="xs">
                    <Group justify="space-between" align="start" wrap="nowrap">
                        <Title order={5} lineClamp={1}>{userName}</Title>
                        {item.priority === 'high' && <Badge color="red" size="xs" variant="light">Высокий</Badge>}
                    </Group>
                    <Text c="gray.6" fw={600} size="sm" mt={-7}>
                        {queueName}
                    </Text>

                    <Group justify="space-between">
                        <Text size="xs" fw={500}>
                            {timeString}
                        </Text>
                        {isPassed && <Badge color="gray" size="xs">Прошел</Badge>}
                    </Group>
                </Stack>
            </Card>
        );
    };

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <Header />

            <AppShell.Main>
                <Container size="80%" py="md" h="calc(100vh - 110px)">
                    <Title order={1} mb="lg">Мои очереди</Title>
                    <Divider size={2} my="sm" />

                    {isLoading ? (
                        <Box style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', height: 'calc(100% - 80px)' }}>
                            {/* Левая колонка - Скелетон */}
                            <Paper withBorder p="md" radius="md" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <Group mb="lg" justify="space-between">
                                    <Skeleton height={28} width={100} radius="sm" />
                                    <Skeleton height={28} width={140} radius="sm" />
                                </Group>
                                <Stack gap="md">
                                    <Skeleton height={20} width={120} radius="sm" mb="xs" />
                                    <Skeleton height={80} radius="md" />
                                    <Skeleton height={80} radius="md" />
                                    <Skeleton height={20} width={120} radius="sm" mt="md" mb="xs" />
                                    <Skeleton height={80} radius="md" />
                                </Stack>
                            </Paper>

                            {/* Правая колонка - Скелетон */}
                            <Paper withBorder p="md" radius="md" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <Group justify="space-between" mb="lg">
                                    <Stack gap="xs">
                                        <Skeleton height={32} width={250} radius="sm" />
                                        <Skeleton height={16} width={150} radius="sm" />
                                    </Stack>
                                    <Skeleton height={28} width={28} radius="sm" />
                                </Group>

                                <SimpleGrid cols={2} spacing="xl" style={{ flex: 1 }}>
                                    <Stack gap="lg">
                                        <Skeleton height={60} radius="md" />
                                        <Skeleton height={40} radius="sm" />
                                        <Divider />
                                        <Skeleton height={200} radius="md" />
                                    </Stack>
                                    <Stack gap="lg">
                                        <Skeleton height={24} width={120} radius="sm" />
                                        <Skeleton height={40} radius="sm" />
                                        <Skeleton height={40} radius="sm" />
                                        <Skeleton height={40} radius="sm" />
                                    </Stack>
                                </SimpleGrid>
                            </Paper>
                        </Box>
                    ) : (
                        <Box style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', height: 'calc(100% - 80px)' }}>
                            <Box style={{ position: 'relative', height: "100%", overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ layout: { type: "spring", stiffness: 300, damping: 30 } }}
                                    style={{ flex: 1, width: '100%', display: 'flex', flexDirection: 'column', minHeight: 0 }}
                                >
                                    <Paper withBorder p="md" radius="md" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', flex: 1 }}>
                                        <Group mb="md" justify="space-between" align="center" wrap="nowrap">
                                            <Title order={3} style={{ whiteSpace: 'nowrap' }}>Визиты</Title>
                                            <Popover position="bottom" withArrow shadow="md" width={400}>
                                                <Popover.Target>
                                                    <Button>Выбрать очередь</Button>
                                                </Popover.Target>
                                                <Popover.Dropdown>
                                                    <MultiSelect
                                                        placeholder="Выберите очереди"
                                                        data={queueOptions}
                                                        value={selectedQueueFilter}
                                                        onChange={setSelectedQueueFilter}
                                                        clearable
                                                        searchable
                                                        variant="unstyled"
                                                        w="100%"
                                                        comboboxProps={{ withinPortal: false }}
                                                    />
                                                </Popover.Dropdown>
                                            </Popover>
                                        </Group>

                                        <ScrollArea style={{ flex: 1 }} type="auto">
                                            <Stack gap="md" pr="xs">
                                                <Paper withBorder p="sm" radius="md">
                                                    <Group justify="space-between" mb="xs" style={{ cursor: 'pointer' }} onClick={() => setExpandedInQueue(!expandedInQueue)}>
                                                        <Text fw={700} size="sm">В очереди ({inQueueList.length})</Text>
                                                        <ActionIcon variant="transparent" size="sm">
                                                            <IconChevronDown size={16} style={{ transform: expandedInQueue ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 200ms ease' }} />
                                                        </ActionIcon>
                                                    </Group>
                                                    <Collapse in={expandedInQueue}>
                                                        <Stack gap="sm">
                                                            {inQueueList.map((req) => {
                                                                const isPassed = req.confirmed_datetime
                                                                    ? dayjs(`${req.confirmed_datetime.date} ${req.confirmed_datetime.time_end}`).isBefore(dayjs())
                                                                    : false;
                                                                return (
                                                                    <QueueCard key={req.id} item={req} isSelected={selectedRequestId === req.id} isPassed={isPassed} />
                                                                );
                                                            })}
                                                            {inQueueList.length === 0 && <Text size="xs" c="dimmed" ta="center">Нет активных визитов</Text>}
                                                        </Stack>
                                                    </Collapse>
                                                </Paper>

                                                <Paper withBorder p="sm" radius="md">
                                                    <Group justify="space-between" mb="xs" style={{ cursor: 'pointer' }} onClick={() => setExpandedWaiting(!expandedWaiting)}>
                                                        <Text fw={700} size="sm">В ожидании ({waitingList.length})</Text>
                                                        <ActionIcon variant="transparent" size="sm">
                                                            <IconChevronDown size={16} style={{ transform: expandedWaiting ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 200ms ease' }} />
                                                        </ActionIcon>
                                                    </Group>
                                                    <Collapse in={expandedWaiting}>
                                                        <Stack gap="sm">
                                                            {waitingList.map((req) => (
                                                                <QueueCard key={req.id} item={req} isSelected={selectedRequestId === req.id} />
                                                            ))}
                                                            {waitingList.length === 0 && <Text size="xs" c="dimmed" ta="center">Нет ожидающих заявок</Text>}
                                                        </Stack>
                                                    </Collapse>
                                                </Paper>
                                            </Stack>
                                        </ScrollArea>
                                    </Paper>
                                </motion.div>
                            </Box>
                            <Box style={{ position: 'relative', height: "100%", overflow: 'hidden' }}>
                                <AnimatePresence mode="wait">
                                    {selectedRequest ? (
                                        <motion.div
                                            key={selectedRequest.id}
                                            initial={{ x: -40, opacity: 0 }}
                                            animate={{ x: 0, opacity: 1 }}
                                            exit={{ x: -40, opacity: 0 }}
                                            transition={{ duration: 0.2, ease: "easeOut" }}
                                            style={{ height: '100%', width: '100%' }}
                                        >
                                            <Paper
                                                withBorder
                                                p={0}
                                                radius="md"
                                                style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', height: '100%' }}
                                            >
                                                <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                                    <Group p="md" pb="xs" justify="space-between" style={{ borderBottom: '1px solid #e5e7eb' }}>
                                                        <Box>
                                                            <Title order={2}>
                                                                {selectedRequest.ownerData
                                                                    ? `${selectedRequest.ownerData.last_name} ${selectedRequest.ownerData.first_name}`
                                                                    : 'Загрузка...'}
                                                            </Title>
                                                            <Text c="gray.6" fw={600} size="sm">
                                                                {selectedRequest.queueData?.name}
                                                            </Text>
                                                        </Box>
                                                        <ActionIcon variant="subtle" color="gray" size="lg" onClick={() => setSelectedRequestId(null)}>
                                                            <IconX size={24} />
                                                        </ActionIcon>
                                                    </Group>

                                                    <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
                                                        <ScrollArea style={{ flex: 1 }} type="auto">
                                                            <Stack gap="lg" p="lg">
                                                                <Paper withBorder p="sm" bg="gray.0" radius="md">
                                                                    <Text size="sm" fw={700} mb={4}>Предпочтения визитера:</Text>
                                                                    <Group gap="xl">
                                                                        <div>
                                                                            <Text size="xs" c="dimmed">Дата</Text>
                                                                            <Text size="sm">{selectedRequest.preferred_datetime.date}</Text>
                                                                        </div>
                                                                        <div>
                                                                            <Text size="xs" c="dimmed">Время</Text>
                                                                            <Text size="sm">
                                                                                {selectedRequest.preferred_datetime.time_start} - {selectedRequest.preferred_datetime.time_end}
                                                                            </Text>
                                                                        </div>
                                                                    </Group>
                                                                </Paper>

                                                                <Stack gap="xs">
                                                                    <Text size="sm" fw={700}>Цель визита</Text>
                                                                    <Text size="sm" style={{ whiteSpace: 'pre-wrap' }}>
                                                                        {selectedRequest.purpose}
                                                                    </Text>
                                                                </Stack>

                                                                <Divider />

                                                                <Stack gap="xs">
                                                                    <Group gap="xs">
                                                                        <IconCalendarTime size={18} />
                                                                        <Text size="sm" fw={700}>
                                                                            {selectedRequest.status === 'pending' ? 'Назначить время' : 'Изменить время'}
                                                                        </Text>
                                                                    </Group>

                                                                    <Paper p="md" withBorder radius="md">
                                                                        <Stack gap="sm">
                                                                            <SimpleGrid cols={2}>
                                                                                <DateInput
                                                                                    value={scheduleDate}
                                                                                    onChange={(value) => setScheduledDate(value as Date | null)}
                                                                                    label="Дата визита"
                                                                                    placeholder="ДД.ММ.ГГГГ"
                                                                                    locale="ru"
                                                                                    minDate={new Date()}
                                                                                    rightSection={<IconCalendar size={16} />}
                                                                                    required
                                                                                />
                                                                                <TimeInput
                                                                                    label="Время начала"
                                                                                    ref={timeInputRef}
                                                                                    value={scheduleTime}
                                                                                    onChange={(e) => setScheduleTime(e.currentTarget.value)}
                                                                                    rightSection={
                                                                                        <ActionIcon
                                                                                            variant="subtle"
                                                                                            color="gray"
                                                                                            onClick={() => timeInputRef.current?.showPicker()}
                                                                                        >
                                                                                            <IconClock size={16} />
                                                                                        </ActionIcon>
                                                                                    }
                                                                                />
                                                                            </SimpleGrid>

                                                                            <NumberInput
                                                                                label="Длительность (мин)"
                                                                                value={scheduleDuration}
                                                                                onChange={(val) => setScheduleDuration(val as number)}
                                                                                min={1}
                                                                            />

                                                                            <Button
                                                                                mt="xs"
                                                                                onClick={handleUpdateTime}
                                                                                loading={isSubmittingTime}
                                                                                disabled={!scheduleDate || !scheduleTime}
                                                                            >
                                                                                {selectedRequest.status === 'pending' ? 'Подтвердить и принять' : 'Обновить время'}
                                                                            </Button>
                                                                        </Stack>
                                                                    </Paper>
                                                                </Stack>

                                                                <Stack gap="xs">
                                                                    <Text size="sm" fw={700}>Приоритет</Text>
                                                                    <SegmentedControl
                                                                        value={selectedRequest.priority === 'low' ? 'Низкий' : selectedRequest.priority === 'medium' ? 'Средний' : 'Высокий'}
                                                                        onChange={handleChangePriority}
                                                                        data={['Низкий', 'Средний', 'Высокий']}
                                                                        fullWidth
                                                                    />
                                                                </Stack>
                                                                <Divider my="sm" />
                                                                <Group justify="end">
                                                                    <Button
                                                                        variant="subtle"
                                                                        color="red"
                                                                        size="sm"
                                                                        onClick={handleReject}
                                                                    >
                                                                        Отменить заявку
                                                                    </Button>
                                                                </Group>
                                                            </Stack>
                                                        </ScrollArea>

                                                        <ScrollArea style={{ flex: 1, borderLeft: '1px solid #e5e7eb' }} type="auto">
                                                            <Stack gap="lg" p="lg">
                                                                <Group gap="xs">
                                                                    <IconActivity size={18} />
                                                                    <Title order={4}>Активность</Title>
                                                                </Group>

                                                                <RequestHistory request={selectedRequest} />

                                                                <Divider label="Новое сообщение" labelPosition="center" />

                                                                <Stack gap="xs">
                                                                    <Textarea
                                                                        placeholder="Напишите комментарий"
                                                                        value={comment}
                                                                        onChange={(e) => setComment(e.currentTarget.value)}
                                                                        minRows={2}
                                                                        autosize
                                                                    />
                                                                    <Button
                                                                        size="sm"
                                                                        variant="light"
                                                                        onClick={handleSendComment}
                                                                        loading={isSubmittingComment}
                                                                        disabled={!comment.trim()}
                                                                    >
                                                                        Отправить
                                                                    </Button>
                                                                </Stack>
                                                            </Stack>
                                                        </ScrollArea>
                                                    </div>
                                                </div>
                                            </Paper>
                                        </motion.div>
                                    ) : (
                                        <motion.div
                                            key="empty"
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                            transition={{ duration: 0.2 }}
                                            style={{ height: '100%', width: '100%' }}
                                        >
                                            <Paper
                                                withBorder
                                                radius="md"
                                                style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                                            >
                                                <Center style={{ flexDirection: 'column', gap: '16px' }}>
                                                    <ThemeIcon variant="light" size={80} radius="xl" color="gray">
                                                        <IconUserOff size={40} />
                                                    </ThemeIcon>
                                                    <Stack gap={0} align="center">
                                                        <Title order={3} c="gray.7">Визитер не выбран</Title>
                                                        <Text c="gray.5">Выберите визитера из списка слева</Text>
                                                    </Stack>
                                                </Center>
                                            </Paper>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </Box>
                        </Box>
                    )}
                </Container>
            </AppShell.Main>
        </AppShell>
    );
};

export default MyQueue;
