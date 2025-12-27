import { useState } from 'react';
import {
    Card,
    Text,
    Badge,
    Group,
    Title,
    Stack,
    Textarea,
    SegmentedControl,
    ScrollArea,
    Box,
    Divider,
    Button,
    ThemeIcon,
    Skeleton
} from '@mantine/core';
import { modals } from '@mantine/modals';
import { notifications } from '@mantine/notifications';
import { IconUser } from '@tabler/icons-react';
import { EnrichedRequest } from '../types/requests';
import { RequestHistory } from './RequestHistory';
import { api } from '../api/ApiClient';

interface ApplicationCardProps {
    request: EnrichedRequest;
    onUpdate: () => void;
}

export function ApplicationCard({ request, onUpdate }: ApplicationCardProps) {
    const [activeTab, setActiveTab] = useState<'info' | 'history'>('info');
    const [comment, setComment] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const getStatusInfo = () => {
        if (request.status === 'pending') return { text: 'Ожидание', color: 'custom-pink' };
        if (request.status === 'accepted') return { text: 'Принято', color: 'green' };
        if (request.status === 'rejected') return { text: 'Отклонено', color: 'red' };
        return { text: 'Неизвестно', color: 'gray' };
    };

    const statusInfo = getStatusInfo();

    const handleSendComment = async () => {
        if (!comment.trim()) return;
        setIsSubmitting(true);
        try {
            await api.request(`/api/v1/requests/${request.id}/comment`, 'POST', { text: comment });
            setComment('');
            notifications.show({ title: 'Успех', message: 'Комментарий добавлен', color: 'green' });
            onUpdate();
        } catch (e) {
            notifications.show({ title: 'Ошибка', message: 'Не удалось отправить комментарий', color: 'red' });
        } finally {
            setIsSubmitting(false);
        }
    };

    const performReject = async () => {
        setIsSubmitting(true);
        try {
            await api.request(`/api/v1/requests/${request.id}/reject`, 'PATCH');
            notifications.show({ title: 'Успех', message: 'Заявка отменена', color: 'green' });
            onUpdate();
        } catch (e) {
            notifications.show({ title: 'Ошибка', message: 'Не удалось отменить заявку', color: 'red' });
        } finally {
            setIsSubmitting(false);
        }
    };

    const openRejectModal = () => modals.openConfirmModal({
        title: 'Отмена заявки',
        centered: true,
        children: (
            <Text size="sm">
                Вы уверены, что хотите отменить эту заявку? Это действие нельзя будет отменить, и заявка будет перемещена в архив.
            </Text>
        ),
        labels: { confirm: 'Да, отменить', cancel: 'Вернуться' },
        confirmProps: { color: 'red' },
        onConfirm: performReject,
    });

    const canReject = !request.is_archived;

    const ownerName = request.ownerData
        ? `${request.ownerData.last_name} ${request.ownerData.first_name}${request.ownerData.patronymic ? ' ' + request.ownerData.patronymic : ''}`
        : 'Загрузка...';

    return (
        <Card shadow="sm" padding="lg" radius="md" withBorder h={600} style={{ display: 'flex', flexDirection: 'column' }}> {/* Чуть увеличил высоту */}

            <Group justify="space-between" mb="xs">
                <Group gap="xs">
                    {request.queueData ? (
                        <Title order={4} lineClamp={1}>{request.queueData.name}</Title>
                    ) : (
                        <Skeleton height={24} width={150} />
                    )}
                </Group>
            </Group>

            <Group gap="xs" mb="sm">
                <ThemeIcon color="gray" variant="transparent" size="sm">
                    <IconUser size={14} />
                </ThemeIcon>
                {request.ownerData ? (
                    <Text size="xs" c="dimmed">{ownerName}</Text>
                ) : (
                    <Skeleton height={16} width={100} />
                )}
            </Group>

            <Group justify="space-between" mb="sm">
                <Group>
                    <Badge color={statusInfo.color} variant="dot">
                        {statusInfo.text}
                    </Badge>
                    {request.is_archived && <Badge color="gray" variant="dot" ml={-10}>Архив</Badge>}
                </Group>
                <SegmentedControl
                    size="xs"
                    value={activeTab}
                    onChange={(val) => setActiveTab(val as 'info' | 'history')}
                    data={[
                        { label: 'Инфо', value: 'info' },
                        { label: 'История', value: 'history' },
                    ]}
                />
            </Group>

            <Divider mb="sm" />

            <ScrollArea style={{ flex: 1 }} type="auto">
                <Box pr="xs" pb="xs">
                    {activeTab === 'info' && (
                        <Stack gap="md">
                            {request.queueData?.description && (
                                <div>
                                    <Text size="sm" fw={700}>Описание очереди:</Text>
                                    <Text size="sm" c="dimmed" lineClamp={3}>
                                        {request.queueData.description}
                                    </Text>
                                </div>
                            )}

                            <div>
                                <Text size="sm" fw={700}>Цель визита:</Text>
                                <Text size="sm">{request.purpose || 'Не указана'}</Text>
                            </div>

                            <div>
                                <Text size="sm" fw={700}>Желаемое время:</Text>
                                <Text size="sm">
                                    {request.preferred_datetime.date} <br />
                                    <Text span c="dimmed" size="xs">
                                        ({request.preferred_datetime.time_start} - {request.preferred_datetime.time_end})
                                    </Text>
                                </Text>
                            </div>

                            {request.status === 'accepted' && request.confirmed_datetime && (
                                <div style={{
                                    backgroundColor: 'var(--mantine-color-green-0)',
                                    padding: '8px',
                                    borderRadius: '8px',
                                    border: '1px solid var(--mantine-color-green-2)'
                                }}>
                                    <Text size="sm" fw={700} c="green.8">Подтвержденное время:</Text>
                                    <Text size="sm" fw={600} c="green.9">
                                        {request.confirmed_datetime.date} <br />
                                        {request.confirmed_datetime.time_start} - {request.confirmed_datetime.time_end}
                                    </Text>
                                </div>
                            )}
                        </Stack>
                    )}

                    {activeTab === 'history' && (
                        <Stack gap="lg">
                            <RequestHistory request={request} />

                            {!request.is_archived && (
                                <Stack gap="xs">
                                    <Text size="sm" fw={500}>Новый комментарий</Text>
                                    <Textarea
                                        placeholder="Напишите что-нибудь..."
                                        value={comment}
                                        onChange={(e) => setComment(e.currentTarget.value)}
                                        minRows={2}
                                        autosize
                                    />
                                    <Button
                                        size="xs"
                                        variant="light"
                                        onClick={handleSendComment}
                                        loading={isSubmitting}
                                        disabled={!comment.trim()}
                                    >
                                        Отправить
                                    </Button>
                                </Stack>
                            )}

                        </Stack>
                    )}
                </Box>
            </ScrollArea>

            {canReject && (
                <>
                    <Divider my="sm" />
                    <Group justify="end">
                        <Button
                            variant="subtle"
                            color="red"
                            size="sm"
                            onClick={openRejectModal}
                            loading={isSubmitting}
                        >
                            Отменить заявку
                        </Button>
                    </Group>
                </>
            )}
        </Card>
    );
}
