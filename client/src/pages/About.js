import { Box, Text, Image, Button, Flex, useToast } from '@chakra-ui/react';
import React from 'react';
import dataReportImg from '../img/dataReport.png';

const reference ='Proma, A. M., Islam, M. S., Ciko, S., Baten, R. A., & Hoque, E. (2022). NADBenchmarks-a compilation of Benchmark Datasets for Machine Learning Tasks related to Natural Disasters.';

const About = () => {
  const toast = useToast();

  const displayToast = () => {
    toast({
      title: 'Following reference has been copied.',
      description: reference,
      status: 'success',
      duration: 5000,
      isClosable: true,
    });
    navigator.clipboard.writeText(reference);
  }


  return (
    <Box w="90%" mt={{base: '80px', '2xl': "100px"}}>
      <Text fontSize="3xl" mt="30px" ml={{base: '480px', '2xl': "650px"}} color="#7AAC35" as="b">
        A climate change benchmark database
      </Text>
      <Flex ml={{base: '200px', '2xl': "300px"}} mt={{base: '80px', '2xl': "100px"}} w="80%">
        <Box textAlign="justify">
          <Text>
            This site facilitates the proccess of searching for natural disaster
            datasets for ML engineers
          </Text>
          <br />
          <Text>
            NaD Benchmarks 2 presents a collection of existing benchmark
            datasets for machine learning models for natural disasters. The
            supported features and individual dataset information are
            specifically included as per feedback collected through user
            interviews.{' '}
          </Text>
          <br />
          <Text>
            NaD Benchmarks 2 is an extention of Benchmark datasets for Machine
            Learning for Natural Disasters as introduced by Proma et al.
          </Text>
          <Button
            bg="#7AAC35"
            color="#FFFFFF"
            variant="solid"
            mt="30px"
            ml="140px"
            onClick={displayToast}
          >
            Copy Reference
          </Button>
        </Box>
        <Image
          src={dataReportImg}
          ml="100px"
          boxSize="500px"
          mb="300px"
          mt="-100px"
        />
      </Flex>
    </Box>
  );
};

export default About;
