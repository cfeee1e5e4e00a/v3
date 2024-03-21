export enum MeasurementType {
    TEMPERATURE = 'temp',
    HUMIDITY = 'humd',
    CURRENT = 'curr',
    TARGET_TEMPERATURE = 'set_temp',
}

export type Measurement<T> = {
    value: T;
    timestamp: string;
};

export type MeasurementsData<T> = Array<Measurement<T>>;
