import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  AppShell,
  SegmentedControl,
  Card,
  Button,
  TextInput,
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
  Menu,
  Paper,
  Box,
  ScrollArea,
} from '@mantine/core';

import { 
    IconClipboardText,
    IconDownload, 
    IconFriends, 
    IconChecklist, 
    IconBellRinging,
    IconTransitionLeft,
    IconMenu2,
    IconChevronDown,
} from '@tabler/icons-react';

interface QueueItem {
  id: number;
  name: string;
  title: string;
  purpose: string;
  date?: string;
  time?: string;
  endTime?: string;
  timeRange?: string;
  duration: number;
  priority?: string;
  email?: string;
  phone?: string;
  hasAttachment?: boolean;
}

interface ActivityItem {
  id: number;
  person: string;
  action: string;
  time: string;
}

export const MyQueue: React.FC = () => {
  const [selectedQueueId, setSelectedQueueId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<string | null>('all');
  const [expandedInQueue, setExpandedInQueue] = useState(true);
  const [expandedWaiting, setExpandedWaiting] = useState(true);
  const [selectedPriority, setSelectedPriority] = useState('Высокий');
  const [editDate, setEditDate] = useState('26/10/2025 14:00');
  const [duration, setDuration] = useState(10);
  const [comment, setComment] = useState('');

  const inQueueData: QueueItem[] = [
    {
      id: 1,
      name: 'Петров Петр Петрович',
      title: 'Устройство в штаб',
      purpose: 'Проходил стажировку в сентябре. хочу устроиться на постоянку, если есть такая возможность',
      date: '26/10/2025',
      time: '14:00',
      endTime: '16:00',
      duration: 15,
      priority: 'Высокий',
      email: 'petpetrov@gmail.com',
      hasAttachment: true,
    },
  ];

  const waitingData: QueueItem[] = [
    {
      id: 2,
      name: 'Олегов Олег Олегович',
      title: 'По поводу отпуска',
      purpose: 'Я уже три года не был в отпуске. Хочу на курорт.',
      timeRange: '16:00 - 19:00',
      duration: 25,
      email: 'olegoleg@gmail.com',
    },
    {
      id: 3,
      name: 'Олегова Екатерина Ильина',
      title: 'Получение премии',
      purpose: 'Получить премию за сентябрь',
      duration: 0,
      email: 'ekaterina@gmail.com',
    },
  ];

  // Активности для каждой карточки
  const activityDataByQueue: { [key: number]: ActivityItem[] } = {
    1: [
      {
        id: 1,
        person: 'Петров Петр Петрович',
        action: 'Добавился в очередь Устройство в штаб',
        time: '2 часа назад',
      },
      {
        id: 2,
        person: 'Иванов Иван Иванович',
        action: 'Утвердил запись на 14:00 часов',
        time: '1 час назад',
      },
      {
        id: 3,
        person: 'Иванов Иван Иванович',
        action: 'Оставил комментарий: возьмите документы с собой',
        time: '30 минут назад',
      },
      {
        id: 4,
        person: 'Иванов Иван Иванович',
        action: 'Завершил приём',
        time: '10 минут назад',
      },
    ],
    2: [
      {
        id: 1,
        person: 'Олегов Олег Олегович',
        action: 'Добавился в очередь По поводу отпуска',
        time: '3 часа назад',
      },
      {
        id: 2,
        person: 'Иванов Иван Иванович',
        action: 'Просмотрел заявку',
        time: '2 часа назад',
      },
    ],
    3: [
      {
        id: 1,
        person: 'Олегова Екатерина Ильина',
        action: 'Добавилась в очередь Получение премии',
        time: '1 день назад',
      },
    ],
  };

  const selectedQueue = [...inQueueData, ...waitingData].find((q) => q.id === selectedQueueId);
  const activityData = selectedQueueId ? activityDataByQueue[selectedQueueId] || [] : [];

  const QueueCard: React.FC<{ item: QueueItem; isSelected?: boolean }> = ({
    item,
    isSelected = false,
  }) => (
    <Card
      p="md"
      radius="md"
      withBorder
      style={{
        cursor: 'pointer',
        backgroundColor: isSelected ? '#fce7f3' : 'white',
        borderColor: isSelected ? '#ec4899' : '#e5e7eb',
        borderWidth: 2,
      }}
      onClick={() => setSelectedQueueId(item.id)}
    >
        <Stack gap="xs">
        <Title order={4}>{item.name}</Title>
        <Text fw={600} size="sm" c="gray.7">
          {item.title}
        </Text>
        <Text size="sm" c="gray.6" lineClamp={2}>
          Цель визита: {item.purpose}
        </Text>
        <Group justify="space-between" align="flex-start">
          <Stack gap={0}>
            <Text size="sm">
              <strong>Дата и время записи:</strong> {item.date || item.timeRange} {item.time || ''}
            </Text>
            <Text size="sm">
              <strong>Длительность встречи:</strong> {item.duration} минут
            </Text>
          </Stack>
          {item.priority === 'Высокий' && (
            <Text size="sm" style={{ whiteSpace: 'nowrap', color: '#C8235A' }}>
              Высокий приоритет
            </Text>
          )}
        </Group>
      </Stack>
    </Card>
  );

  return (
    <AppShell
            header={{ height: 70 }}
            padding="md"
    >
            <AppShell.Header>
                <Container size="100%" h="100%">
                    <Group h="100%" px="md" justify="space-between">
                        <Title order={2} c="#e91e63">К Телеком</Title>
                        <Group>
                            <Button variant="outline" color='#b9bbb5ff'>Вход</Button>
                            <Button>Регистрация</Button>
                            <Menu shadow="md" width={200}>
                                <Menu.Target>
                                    <IconMenu2 size={32}/>
                                </Menu.Target>

                                <Menu.Dropdown style={{zIndex: 1001}}>
                                    <Menu.Item component={Link} to="/" leftSection={<IconClipboardText size={16} />}>
                                        Доступные очереди
                                    </Menu.Item>
                                    <Menu.Item component={Link} to="/my-queue" leftSection={<IconFriends size={16} />}>
                                        Мои очереди
                                    </Menu.Item>
                                    <Menu.Item component={Link} to="/my-application" leftSection={<IconChecklist size={16} />}>
                                        Мои заявки
                                    </Menu.Item>
                                    <Menu.Item leftSection={<IconBellRinging size={16} />}>
                                        Настройки уведомлений
                                    </Menu.Item>
                                    <Menu.Item color="red" leftSection={<IconTransitionLeft size={16} />}>
                                        Выход
                                    </Menu.Item>
                                </Menu.Dropdown>
                            </Menu>
                        </Group>
                    </Group>
                </Container>
            </AppShell.Header>

    <AppShell.Main>
        
        <Container size="80%" py="md">
            <Title order={1} mb="lg">Мои очереди</Title>

            <Divider size={2} my="sm" />

            <Box
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr 1fr',
              gap: '20px',
              height: 'calc(100vh - 214px)',
            }}
          >

            <Paper
              withBorder
              p="md"
              radius="md"
              style={{
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
              }}
            >
              <Group mb="md" align="flex-start">
                <SegmentedControl
                  value={activeTab}
                  onChange={setActiveTab}
                  data={[
                    { label: 'Все', value: 'all' },
                    { label: 'Очередь', value: 'queue' },
                    { label: 'Ожидание', value: 'waiting' },
                  ]}
                  style={{ flex: 1 }}
                />
                <Button size="sm" rightSection={<IconChevronDown size={16} />}>
                  Выбрать очередь
                </Button>
              </Group>
              
              <ScrollArea style={{ flex: 1 }} type="auto">
                <Stack gap="md" pr="md">

                  <Paper withBorder p="md" radius="md">
                    <Group justify="space-between" mb="md">
                      <Text fw={600} style={{ cursor: 'pointer' }} onClick={() => setExpandedInQueue(!expandedInQueue)}>
                        В очереди
                      </Text>
                      <ActionIcon
                        variant="transparent"
                        onClick={() => setExpandedInQueue(!expandedInQueue)}
                      >
                        <IconChevronDown
                          size={16}
                          style={{
                            transform: expandedInQueue ? 'rotate(180deg)' : 'rotate(0deg)',
                            transition: 'transform 200ms ease',
                          }}
                        />
                      </ActionIcon>
                    </Group>
                    <Collapse in={expandedInQueue}>
                      <Stack gap="md">
                        {inQueueData.map((item) => (
                          <QueueCard key={item.id} item={item} />
                        ))}
                      </Stack>
                    </Collapse>
                  </Paper>

                  <Paper withBorder p="md" radius="md">
                    <Group justify="space-between" mb="md">
                      <Text fw={600} style={{ cursor: 'pointer' }} onClick={() => setExpandedWaiting(!expandedWaiting)}>
                        В ожидании
                      </Text>
                      <ActionIcon
                        variant="transparent"
                        onClick={() => setExpandedWaiting(!expandedWaiting)}
                      >
                        <IconChevronDown
                          size={16}
                          style={{
                            transform: expandedWaiting ? 'rotate(180deg)' : 'rotate(0deg)',
                            transition: 'transform 200ms ease',
                          }}
                        />
                      </ActionIcon>
                    </Group>
                    <Collapse in={expandedWaiting}>
                      <Stack gap="md">
                        {waitingData.map((item) => (
                          <QueueCard key={item.id} item={item} />
                        ))}
                      </Stack>
                    </Collapse>
                  </Paper>
                </Stack>
              </ScrollArea>
            </Paper>

            <Paper
              withBorder
              p="md"
              radius="md"
              style={{
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
              }}
            >
              <ScrollArea style={{ flex: 1 }} type="auto">
                {selectedQueue ? (
                  <Stack gap="md" pr="md">
                    <div>
                      <Title order={2}>{selectedQueue.name}</Title>
                      <Text c="gray.6" fw={600} mt={4}>
                        {selectedQueue.title}
                      </Text>
                    </div>

                    <Stack gap="xs">
                      <div>
                        <Text size="sm" c="gray.7">
                          <strong>Email</strong>
                        </Text>
                        <Text size="sm">{selectedQueue.email}</Text>
                      </div>
                    </Stack>

                    <div>
                      <Text size="sm" fw={600} c="gray.7" mb={4}>
                        Цель визита
                      </Text>
                      <Text size="sm">{selectedQueue.purpose}</Text>
                    </div>

                    <div>
                      <Text size="sm">
                        <strong>Желаемые дата и время посещения:</strong> 
                        <p>{selectedQueue.date}{' '}
                        {selectedQueue.time} - {selectedQueue.endTime}</p>
                      </Text>
                    </div>

                    {selectedQueue.hasAttachment && (
                      <Group justify="start" mb="md">
                        <Button
                          leftSection={<IconDownload size={16} />}
                        >
                          Скачать приложенный файл
                        </Button>
                      </Group>
                    )}

                    <Stack gap="sm">
                      <TextInput
                        label="Дата и время записи"
                        value={editDate}
                        onChange={(e) => setEditDate(e.currentTarget.value)}
                      />

                      <Stack gap="xs">
                        <Text size="md" fw={600}>
                          Приоритет
                        </Text>
                        <SegmentedControl 
                          value={selectedPriority}
                          onChange={setSelectedPriority}
                          data={[
                            { label: 'Низкий', value: 'Низкий' },
                            { label: 'Средний', value: 'Средний' },
                            { label: 'Высокий', value: 'Высокий' },
                          ]}
                          fullWidth
                        />
                      </Stack>

                      <NumberInput
                        label="Длительность визита в минутах"
                        value={duration}
                        onChange={(val) => setDuration(val as number)}
                        min={1}
                      />
                    </Stack>

                    <Group grow>
                      <Button fullWidth>
                        Изменить запись
                      </Button>
                      <Button variant="default" fullWidth>
                        Отменить запись
                      </Button>
                    </Group>
                  </Stack>
                ) : (
                  <Text c="gray.5" ta="center" mt="xl">
                    Выберите заявку для просмотра деталей
                  </Text>
                )}
              </ScrollArea>
            </Paper>

            <Paper
              withBorder
              p="md"
              radius="md"
              style={{
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
              }}
            >
              <Group justify="space-between" mb="md">
                <Title order={3}>Активность</Title>
                <Button
                  size="sm"
                  rightSection={<IconChevronDown size={16} />}
                >
                  Выбрать событие
                </Button>
              </Group>

              <ScrollArea style={{ flex: 1 }} type="auto">
                {selectedQueue && activityData.length > 0 ? (
                  <Box pr="md">
                    <Timeline active={activityData.length} bulletSize={20} lineWidth={4}>
                      {activityData.map((item) => (
                        <Timeline.Item
                          key={item.id}
                          title={<Text fw={600}>{item.person}</Text>}
                        >
                          <Text c="dimmed" size="sm" mt={4}>
                            {item.action}
                          </Text>
                          <Text size="xs" mt={4} c="gray.5">
                            {item.time}
                          </Text>
                        </Timeline.Item>
                      ))}
                    </Timeline>
                    
                    <Stack gap="sm" mt="md">
                      <Text size="sm" fw={600}>
                        Комментарий
                      </Text>
                      <Textarea
                        placeholder="Укажите важные детали или пожелания"
                        value={comment}
                        onChange={(e) => setComment(e.currentTarget.value)}
                        minRows={3}
                        size="sm"
                      />
                    </Stack>
                  </Box>
                ) : (
                  <Text c="gray.5" ta="center" mt="xl">
                    Выберите заявку для просмотра активности
                  </Text>
                )}
              </ScrollArea>
            </Paper>
          </Box>
        </Container>
      </AppShell.Main>
    </AppShell>
  );
};

export default MyQueue;
