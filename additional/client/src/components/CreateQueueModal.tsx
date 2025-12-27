import { useState, useRef } from 'react';
import { Drawer, Stack, TextInput, Textarea, SimpleGrid, NumberInput, Button, ActionIcon, Text } from '@mantine/core'; // Используем Drawer
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

    return (
        <Drawer
            opened={opened}
            onClose={onClose}
            title="Создать очередь"
            position="right"
            padding="xl"
            offset={8}
            radius="md"
            size={400}
            overlayProps={{ backgroundOpacity: 0.5, blur: 4 }}
            transitionProps={{ duration: 200, timingFunction: 'ease' }}
        >
            <Stack gap="md">
                <TextInput 
                    label="Название"
                    placeholder="Введите название очереди"
                    required 
                    value={name} 
                    onChange={(e) => setName(e.currentTarget.value)} 
                />
                <Textarea 
                    label="Описание"
                    placeholder="Введите описание очереди"
                    minRows={3} 
                    value={description} 
                    onChange={(e) => setDescription(e.currentTarget.value)} 
                />
                <SimpleGrid cols={2}>
                    <TimeInput 
                        label="Начало приёма" 
                        ref={startRef} 
                        rightSection={pickerControl(startRef)} 
                        value={startTime} 
                        onChange={(e) => setStartTime(e.currentTarget.value)} 
                        required 
                    />
                    <TimeInput 
                        label="Окончание приема" 
                        ref={endRef} 
                        rightSection={pickerControl(endRef)} 
                        value={endTime} 
                        onChange={(e) => setEndTime(e.currentTarget.value)} 
                        required 
                    />
                </SimpleGrid>
                <NumberInput 
                    label="Период автоочистки (дней)" 
                    required 
                    min={1} 
                    value={autocloseDays} 
                    onChange={setAutocloseDays} 
                />
                <Text size="xs" c="dimmed" mt={-5}>Через указанное количество дней запрос попадет в архив.</Text>
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
        </Drawer>
    );
}
