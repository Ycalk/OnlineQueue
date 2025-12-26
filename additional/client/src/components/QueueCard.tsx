import { useState, useRef } from 'react';
import { Card, Text, Badge, Group, Title, Stack, Button, TextInput, Textarea, SimpleGrid, ActionIcon } from '@mantine/core';
import { DateInput, TimeInput } from '@mantine/dates';
import { IconChevronUp, IconChevronDown, IconCalendar, IconClock, IconCheck, IconX } from '@tabler/icons-react';
import { motion, AnimatePresence } from 'framer-motion';
import { notifications } from '@mantine/notifications';
import { api } from '../api/ApiClient';

export interface QueueDisplay {
    id: string;
    owner_id: string;
    name: string;
    description: string | null;
    cleanup_period_days: number;
    reception_time_start: string;
    reception_time_end: string;
    requests_avg_duration_seconds: number | null;
    is_active: boolean;
    ownerName: string;
}

interface CreateRequestPayload {
    queue_id: string;
    purpose: string;
    preferred_date: string; // YYYY-MM-DD
    preferred_time_start: string; // HH:mm
    preferred_time_end: string;   // HH:mm
}

interface QueueCardProps {
    queue: QueueDisplay;
    isOpen: boolean;
    onToggle: () => void;
}

export function QueueCard({ queue, isOpen, onToggle }: QueueCardProps) {
    const [visitDate, setVisitDate] = useState<Date | null>(null);
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [visitPurpose, setVisitPurpose] = useState('');

    const [isSubmitting, setIsSubmitting] = useState(false);

    const startTimeRef = useRef<HTMLInputElement>(null);
    const endTimeRef = useRef<HTMLInputElement>(null);

    const isFormValid = visitDate !== null && startTime !== '' && endTime !== '' && visitPurpose.trim().length > 0;

    const pickerControl = (ref: React.RefObject<HTMLInputElement | null>) => (
        <ActionIcon variant="subtle" color="gray" onClick={() => ref.current?.showPicker()}>
            <IconClock size={16} />
        </ActionIcon>
    );

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

    const handleSubmit = async () => {
        if (!visitDate) return;

        if (!localStorage.getItem('access_token')) {
            notifications.show({
                title: 'Ошибка',
                message: 'Необходимо авторизоваться',
                color: 'red',
            });
            return;
        }

        try {
            setIsSubmitting(true);

            const payload: CreateRequestPayload = {
                queue_id: queue.id,
                purpose: visitPurpose,
                preferred_date: formatDate(visitDate),
                preferred_time_start: startTime,
                preferred_time_end: endTime
            };

            await api.request('/api/v1/requests', 'POST', payload);

            notifications.show({
                title: 'Заявка отправлена',
                message: `Вы успешно записались в очередь "${queue.name}"`,
                color: 'green',
                icon: <IconCheck size={18} />,
            });

            setVisitDate(null);
            setStartTime('');
            setEndTime('');
            setVisitPurpose('');
            onToggle();

        } catch (error: any) {
            console.error('Ошибка при записи:', error);
            notifications.show({
                title: 'Ошибка',
                message: error.message || 'Не удалось отправить заявку',
                color: 'red',
                icon: <IconX size={18} />,
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <motion.div
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ layout: { type: "spring", stiffness: 300, damping: 30 } }}
            style={{ width: '100%' }}
        >
            <Card shadow={isOpen ? 'md' : 'sm'} padding="lg" radius="md" withBorder style={{ borderColor: isOpen ? '#e91e63' : undefined, transition: 'border-color 0.2s', overflow: 'hidden' }}>
                <Group justify="space-between" mb="xs">
                    <Badge color={queue.is_active ? '#5FBF24' : '#FA5252'} variant="dot">
                        {queue.is_active ? 'Активна' : 'Неактивна'}
                    </Badge>
                </Group>

                <Title order={4} mb="md" lineClamp={1}>{queue.name}</Title>

                <Stack gap="xs" mb="lg">
                    <Group justify="space-between">
                        <Text size="sm" c="dimmed">Владелец:</Text>
                        <Text size="sm" fw={500}>{queue.ownerName}</Text>
                    </Group>
                    <Group justify="space-between">
                        <Text size="sm" c="dimmed">Время приёма:</Text>
                        <Text size="sm" fw={500}>
                            {queue.reception_time_start.slice(0, 5)} - {queue.reception_time_end.slice(0, 5)}
                        </Text>
                    </Group>
                </Stack>

                <Button fullWidth variant={isOpen ? 'light' : 'outline'} onClick={onToggle} rightSection={isOpen ? <IconChevronUp size={16} /> : <IconChevronDown size={16} />}>
                    {isOpen ? 'Скрыть' : 'Записаться'}
                </Button>

                <AnimatePresence initial={false}>
                    {isOpen && (
                        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }}>
                            <div style={{ paddingTop: 16, marginTop: 16, borderTop: '1px solid #eee' }}>
                                <Text size="sm" mb="md">{queue.description || 'Нет описания'}</Text>
                                <Title order={5} mb="sm" size="sm">Форма записи</Title>
                                <Stack gap="sm">
                                    <DateInput
                                        value={visitDate}
                                        onChange={(val) => setVisitDate(val as Date | null)}
                                        label="Дата визита"
                                        placeholder="ДД.ММ.ГГГГ"
                                        locale="ru"
                                        minDate={new Date()}
                                        rightSection={<IconCalendar size={16} />}
                                        required
                                    />
                                    <SimpleGrid cols={2}>
                                        <TimeInput label="Начало (время)" ref={startTimeRef} rightSection={pickerControl(startTimeRef)} placeholder="10:00" value={startTime} onChange={(e) => setStartTime(e.currentTarget.value)} required />
                                        <TimeInput label="Окончание (время)" ref={endTimeRef} rightSection={pickerControl(endTimeRef)} placeholder="10:15" value={endTime} onChange={(e) => setEndTime(e.currentTarget.value)} required />
                                    </SimpleGrid>
                                    <Text size="xs" c="dimmed" mt={-5}>Укажите желаемый интервал времени приёма.</Text>
                                    <Textarea label="Цель визита" placeholder="Кратко опишите вопрос" minRows={2} value={visitPurpose} onChange={(e) => setVisitPurpose(e.currentTarget.value)} required />

                                    <Button
                                        fullWidth
                                        mt="xs"
                                        disabled={!isFormValid}
                                        onClick={handleSubmit}
                                        loading={isSubmitting}
                                    >
                                        Записаться
                                    </Button>
                                </Stack>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </Card>
        </motion.div>
    );
}
