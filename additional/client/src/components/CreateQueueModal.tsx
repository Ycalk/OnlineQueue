import { useState, useRef } from 'react';
import { Paper, Group, Title, ActionIcon, Stack, TextInput, Textarea, SimpleGrid, NumberInput, Button, Box } from '@mantine/core';
import { TimeInput } from '@mantine/dates';
import { IconClock } from '@tabler/icons-react';


export interface CreateQueuePayload {
    name: string;
    description: string | null;
    cleanup_period_days: number;
    reception_time_start: string;
    reception_time_end: string;
}

interface CreateQueueModalProps {
    opened: boolean;
    onClose: () => void;
    onSubmit: (data: CreateQueuePayload) => void;
    isLoading?: boolean;
}

export function CreateQueueModal({ opened, onClose, onSubmit, isLoading = false }: CreateQueueModalProps) {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [autocloseDays, setAutocloseDays] = useState<string | number>(7);

    const startRef = useRef<HTMLInputElement>(null);
    const endRef = useRef<HTMLInputElement>(null);

    const pickerControl = (ref: React.RefObject<HTMLInputElement | null>) => (
        <ActionIcon variant="subtle" color="gray" onClick={() => ref.current?.showPicker()}>
            <IconClock size={16} />
        </ActionIcon>
    );

    const handleCreate = () => {
        const payload: CreateQueuePayload = {
            name,
            description: description.trim() === '' ? null : description,
            cleanup_period_days: Number(autocloseDays) || 7,
            reception_time_start: startTime,
            reception_time_end: endTime,
        };

        onSubmit(payload);
    };

    if (!opened) return null;

    return (
        <>
            <Box onClick={onClose} style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.4)', zIndex: 200 }} />
            <Paper shadow="xl" p="xl" style={{ position: 'fixed', top: 0, right: 0, width: 400, height: '100%', zIndex: 201 }}>
                <Group justify="space-between" mb="lg">
                    <Title order={3}>Создать очередь</Title>
                    <ActionIcon variant="transparent" onClick={onClose}>✕</ActionIcon>
                </Group>
                <Stack gap="md">
                    <TextInput label="Название" required value={name} onChange={(e) => setName(e.currentTarget.value)} />
                    <Textarea label="Описание" minRows={3} value={description} onChange={(e) => setDescription(e.currentTarget.value)} />
                    <SimpleGrid cols={2}>
                        <TimeInput label="Начало приёма" ref={startRef} rightSection={pickerControl(startRef)} value={startTime} onChange={(e) => setStartTime(e.currentTarget.value)} required />
                        <TimeInput label="Конец приёма" ref={endRef} rightSection={pickerControl(endRef)} value={endTime} onChange={(e) => setEndTime(e.currentTarget.value)} required />
                    </SimpleGrid>
                    <NumberInput label="Период автоочистки (дней)" required min={1} value={autocloseDays} onChange={setAutocloseDays} />

                    <Button
                        onClick={handleCreate}
                        fullWidth
                        mt="md"
                        loading={isLoading}
                        disabled={!name || !startTime || !endTime}
                    >
                        Создать
                    </Button>
                </Stack>
            </Paper>
        </>
    );
}
